"""Pillar 2 — isolated, performant compute for building, testing and validating.

A step runs against a *detached worktree of an immutable commit*, with an
environment that was declared rather than inherited, under resource limits, with a
timeout that kills the whole process group, and with its output scrubbed before it
is ever written down.

Two backends:

  container  `docker run` with all capabilities dropped, no network, a non-root
             uid, a read-only root filesystem, a pids limit and a memory cap
  local      the same process tree, isolated by `setrlimit` and a fresh session,
             with the environment allowlisted and the workdir confined

`auto` picks container when a runtime is present. What it picked is recorded in the
result, the ledger and the attestation — never inferred from configuration. A local
run does not isolate the network, and saying otherwise in a provenance record would
make the record a lie.

Derived from the corpus:
  archon-subprocess-stream-lifecycle (coleam00/Archon) — process exit, stream close,
      abort and timeout escalation are concurrent events that race. `_terminate_group`
      and reading the logs only after the wait returns come from this.
  mcp-enforce-resource-caps (awslabs/mcp) — bound inputs and outputs, and clean up on
      timeout or eviction. The rlimits, the output cap and the pids limit are this
      rule in three places.
  volcano-use-controlled-concurrency-patterns (volcano-sh/volcano) — concurrency is
      declared and bounded, never incidental.
  azure-cli-secure-untrusted-boundaries (Azure/azure-cli) — for subprocess execution,
      never rely on naive quoting; pass arguments as separate items.
  aidlc-workflows-sandbox-config-boundary — the sandbox's configuration is part of
      the security boundary; resolve it once and report it, do not re-derive it at
      each use site.
  aidlc-workflows-secure-path-confinement — drop capabilities, run as the calling
      uid, cap resources, and scrub credentials from stdout/stderr before
      returning them.
  aidlc-workflows-explicit-environment-contracts — a step sees the variables it
      declared. Inheriting `os.environ` wholesale is how a token reaches a build
      log and how a build passes on one machine only.
  aidlc-workflows-fail-loudly-degrade-safely — the degraded backend is named in
      the record. `auto` degrades; `container` refuses.
"""

from __future__ import annotations

import glob as globlib
import os
import resource
import shlex
import shutil
import signal
import subprocess
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, Sequence

from .digest import digest_json, digest_text
from .errors import BackendUnavailable, ExecutionError, StepTimeout, UsageError
from .paths import ensure_dir, resolve_within
from .scrub import scrub, scrub_argv, scrub_env
from .workspace import atomic_write_bytes

TRUNCATION_NOTICE = "\n... [awesome-harness truncated {dropped} bytes of output] ...\n"


# --------------------------------------------------------------------------- #
# Step model
# --------------------------------------------------------------------------- #

@dataclass(frozen=True)
class Output:
    """A path or glob, relative to the step's working directory, to capture."""

    path: str
    allow_empty: bool = False
    optional: bool = False

    @classmethod
    def parse(cls, raw: Any) -> "Output":
        if isinstance(raw, str):
            return cls(path=raw)
        if isinstance(raw, dict) and "path" in raw:
            return cls(
                path=str(raw["path"]),
                allow_empty=bool(raw.get("allow_empty", False)),
                optional=bool(raw.get("optional", False)),
            )
        raise UsageError(f"output must be a string or an object with a 'path': {raw!r}")


@dataclass(frozen=True)
class Step:
    id: str
    run: tuple[str, ...]
    cwd: str = "."
    timeout_seconds: float | None = None
    # Globs, relative to the repository root, whose content decides cache validity.
    inputs: tuple[str, ...] = ()
    outputs: tuple[Output, ...] = ()
    # Commands whose stdout fingerprints a tool version, e.g. `python3 --version`.
    # In the cache key, because a step's result depends on the toolchain even when
    # every tracked file is identical.
    tools: tuple[str, ...] = ()
    env: dict[str, str] = field(default_factory=dict)
    cacheable: bool = True
    allow_network: bool = False
    # A step may fail without failing the phase — for probes and advisory checks.
    allow_failure: bool = False

    @classmethod
    def parse(cls, raw: dict[str, Any]) -> "Step":
        if not isinstance(raw, dict):
            raise UsageError(f"step must be an object: {raw!r}")
        for required in ("id", "run"):
            if required not in raw:
                raise UsageError(f"step is missing {required!r}: {raw!r}")
        run = raw["run"]
        # A list, never a string. Accepting a string would mean either running a
        # shell (injection) or guessing at word splitting (wrong for paths with
        # spaces). `shlex.split` is offered only for the documented convenience of a
        # plan written by hand, and it never sees a shell.
        argv = tuple(str(a) for a in run) if isinstance(run, list) else tuple(shlex.split(str(run)))
        if not argv:
            raise UsageError(f"step {raw['id']!r} has an empty command")
        return cls(
            id=str(raw["id"]),
            run=argv,
            cwd=str(raw.get("cwd", ".")),
            timeout_seconds=float(raw["timeout_seconds"]) if raw.get("timeout_seconds") else None,
            inputs=tuple(str(i) for i in raw.get("inputs", [])),
            outputs=tuple(Output.parse(o) for o in raw.get("outputs", [])),
            tools=tuple(str(t) for t in raw.get("tools", [])),
            env={str(k): str(v) for k, v in (raw.get("env") or {}).items()},
            cacheable=bool(raw.get("cacheable", True)),
            allow_network=bool(raw.get("allow_network", False)),
            allow_failure=bool(raw.get("allow_failure", False)),
        )

    def identity(self) -> dict[str, Any]:
        """The part of a step that belongs in a cache key."""
        return {
            "id": self.id,
            "run": list(self.run),
            "cwd": self.cwd,
            "env": dict(sorted(self.env.items())),
            "outputs": [o.path for o in sorted(self.outputs, key=lambda o: o.path)],
            "allow_network": self.allow_network,
        }


@dataclass
class Limits:
    memory_mb: int = 2048
    # Total CPU time one step may consume (RLIMIT_CPU), distinct from...
    cpu_seconds: int = 600
    # ...how many cores it may consume it on (container --cpus).
    cpus: float = 2.0
    output_bytes: int = 8 << 20
    open_files: int = 1024
    processes: int = 256
    wall_seconds: float = 900.0

    def to_json(self) -> dict[str, Any]:
        return {
            "memory_mb": self.memory_mb,
            "cpu_seconds": self.cpu_seconds,
            "cpus": self.cpus,
            "output_bytes": self.output_bytes,
            "open_files": self.open_files,
            "processes": self.processes,
            "wall_seconds": self.wall_seconds,
        }


@dataclass
class RawResult:
    exit_code: int
    duration_ms: int
    stdout: str
    stderr: str
    truncated: bool
    timed_out: bool
    redactions: list[str]
    isolation: dict[str, Any]


# --------------------------------------------------------------------------- #
# Environment
# --------------------------------------------------------------------------- #

def build_env(
    *,
    allow: Sequence[str],
    fixed: dict[str, str],
    step_env: dict[str, str],
    home: Path,
) -> dict[str, str]:
    """Construct the step environment from an allowlist, not from inheritance.

    Order matters: allowlisted parent values first, then the deterministic overlay,
    then the step's own declarations. A step can therefore pin something the
    machine got wrong, but nothing undeclared can reach it.
    """
    env = {name: os.environ[name] for name in allow if name in os.environ}
    env.update(fixed)
    env.update(step_env)
    # A step that writes to the real ~ is a step whose second run differs from its
    # first. Point HOME at the run folder.
    env["HOME"] = str(home)
    env.setdefault("TMPDIR", str(home / "tmp"))
    env.setdefault("PATH", os.environ.get("PATH", "/usr/local/bin:/usr/bin:/bin"))
    return env


def env_fingerprint(env: dict[str, str]) -> dict[str, str]:
    """Name -> digest of value.

    The cache key needs to change when an environment value changes, but the cache
    entry is a file on disk that may be inspected or shipped. Digests give the first
    without ever writing the second.
    """
    return {name: digest_text(value) for name, value in sorted(env.items())}


# --------------------------------------------------------------------------- #
# Backends
# --------------------------------------------------------------------------- #

class Sandbox:
    name = "abstract"

    def available(self) -> tuple[bool, str]:
        raise NotImplementedError

    def isolation(self, step: Step, limits: Limits) -> dict[str, Any]:
        raise NotImplementedError

    def execute(
        self,
        step: Step,
        *,
        workdir: Path,
        env: dict[str, str],
        limits: Limits,
        run_dir: Path,
    ) -> RawResult:
        raise NotImplementedError


class LocalSandbox(Sandbox):
    """Same-kernel isolation: new session, rlimits, allowlisted env, confined cwd.

    Honest about its ceiling. The filesystem outside the worktree is reachable and
    the network is not namespaced, so `isolation()` says so in the words that end up
    in the attestation.
    """

    name = "local"

    def available(self) -> tuple[bool, str]:
        return True, "always available"

    def isolation(self, step: Step, limits: Limits) -> dict[str, Any]:
        return {
            "backend": "local",
            "process_group": "new session",
            "rlimits": limits.to_json(),
            "environment": "allowlisted",
            "filesystem": "worktree cwd; host filesystem reachable",
            "network": "host (not isolated)",
            "user": f"{os.getuid()}:{os.getgid()}",
        }

    def execute(self, step, *, workdir, env, limits, run_dir):  # type: ignore[no-untyped-def]
        cwd = resolve_within(workdir, step.cwd) if step.cwd not in ("", ".") else workdir
        ensure_dir(Path(env["TMPDIR"]))
        stdout_path = run_dir / f"{step.id}.stdout"
        stderr_path = run_dir / f"{step.id}.stderr"
        wall = step.timeout_seconds or limits.wall_seconds

        def apply_limits() -> None:  # pragma: no cover - runs in the child
            # RLIMIT_AS rather than RLIMIT_DATA: it covers mmap, which is how a
            # runaway allocation actually arrives. 0 disables, because some runtimes
            # (JVM, sanitizers) reserve enormous address space up front and would
            # die on a limit that is fine for everything else.
            if limits.memory_mb:
                as_bytes = limits.memory_mb * 1024 * 1024
                resource.setrlimit(resource.RLIMIT_AS, (as_bytes, as_bytes))
            if limits.cpu_seconds:
                resource.setrlimit(resource.RLIMIT_CPU, (limits.cpu_seconds, limits.cpu_seconds + 5))
            if limits.open_files:
                resource.setrlimit(resource.RLIMIT_NOFILE, (limits.open_files, limits.open_files))
            if limits.processes:
                resource.setrlimit(resource.RLIMIT_NPROC, (limits.processes, limits.processes))
            if limits.output_bytes:
                # A hard stop on file size, so a step cannot fill the disk faster
                # than the harness can notice.
                cap = max(limits.output_bytes * 4, 64 << 20)
                resource.setrlimit(resource.RLIMIT_FSIZE, (cap, cap))
            resource.setrlimit(resource.RLIMIT_CORE, (0, 0))

        started = time.monotonic()
        timed_out = False
        with open(stdout_path, "wb") as out, open(stderr_path, "wb") as err:
            try:
                process = subprocess.Popen(  # noqa: S603 - argv list, shell never involved
                    list(step.run),
                    cwd=cwd,
                    env=env,
                    stdout=out,
                    stderr=err,
                    stdin=subprocess.DEVNULL,
                    # Its own session, so a timeout can kill the whole tree instead
                    # of orphaning grandchildren that keep holding the CPU.
                    start_new_session=True,
                    preexec_fn=apply_limits,
                    close_fds=True,
                )
            except FileNotFoundError as exc:
                raise ExecutionError(
                    f"step {step.id!r}: command not found: {step.run[0]}",
                    hint="the step's argv[0] must exist on PATH inside the sandbox",
                ) from exc
            except PermissionError as exc:
                raise ExecutionError(f"step {step.id!r}: not executable: {step.run[0]}") from exc

            try:
                exit_code = process.wait(timeout=wall)
            except subprocess.TimeoutExpired:
                timed_out = True
                exit_code = _terminate_group(process)

        duration_ms = int((time.monotonic() - started) * 1000)
        stdout, stderr, truncated, redactions = _collect_output(stdout_path, stderr_path, limits)
        result = RawResult(
            exit_code=exit_code,
            duration_ms=duration_ms,
            stdout=stdout,
            stderr=stderr,
            truncated=truncated,
            timed_out=timed_out,
            redactions=redactions,
            isolation=self.isolation(step, limits),
        )
        if timed_out:
            raise StepTimeout(
                f"step {step.id!r} exceeded its {wall:g}s wall clock and was killed",
                hint="raise timeout_seconds on the step, or make the step do less",
            )
        return result


class ContainerSandbox(Sandbox):
    """`docker run` with the whole hardening set applied every time.

    Every flag here corresponds to a way an untrusted build step gets out:
    capabilities, privilege escalation, a writable root filesystem, the network,
    fork bombs, memory exhaustion, and running as root inside a bind mount that is
    owned by you outside it.
    """

    name = "container"

    def __init__(self, image: str, runtime: str = "docker") -> None:
        self.image = image
        self.runtime = runtime
        # Resolved at most once per process. `isolation()` is called per step and its
        # result reaches the cache key, so re-probing would let the value move between
        # two steps of one run — and running a step is itself capable of changing it,
        # because a `docker run` on a missing image pulls it and thereby creates the
        # digest that was absent a moment earlier.
        self._digest: str | None = None
        self._digest_resolved = False

    def available(self) -> tuple[bool, str]:
        if not shutil.which(self.runtime):
            return False, f"{self.runtime} is not on PATH"
        probe = subprocess.run(  # noqa: S603
            [self.runtime, "version", "--format", "{{.Server.Version}}"],
            capture_output=True,
            text=True,
            timeout=20,
        )
        if probe.returncode != 0:
            detail = (probe.stderr or probe.stdout or "").strip().splitlines()
            return False, f"{self.runtime} daemon unreachable: {detail[0] if detail else '?'}"
        return True, f"{self.runtime} server {probe.stdout.strip()}"

    def image_digest(self) -> str | None:
        """The image's repo digest, for the cache key and the attestation.

        A tag is a mutable pointer. Keying a cache on `python:3.11-slim` means the
        cache silently spans two different toolchains the day the tag moves.

        Memoized, and that is load-bearing rather than an optimisation: an unmemoized
        probe returns None before the first `docker run` and a digest afterwards, so
        two identical runs would compute two different keys and the cache would never
        hit. Resolve once, report the same answer for the life of the process.
        """
        if self._digest_resolved:
            return self._digest
        self._digest_resolved = True
        try:
            probe = subprocess.run(  # noqa: S603
                [self.runtime, "image", "inspect", "--format", "{{index .RepoDigests 0}}", self.image],
                capture_output=True,
                text=True,
                timeout=30,
            )
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return None
        self._digest = (probe.stdout.strip() or None) if probe.returncode == 0 else None
        return self._digest

    def isolation(self, step: Step, limits: Limits) -> dict[str, Any]:
        return {
            "backend": "container",
            "runtime": self.runtime,
            "image": self.image,
            "image_digest": self.image_digest(),
            "capabilities": "all dropped",
            "no_new_privileges": True,
            "root_filesystem": "read-only",
            "network": "host" if step.allow_network else "none",
            "user": f"{os.getuid()}:{os.getgid()}",
            "pids_limit": limits.processes,
            "memory_mb": limits.memory_mb,
        }

    def execute(self, step, *, workdir, env, limits, run_dir):  # type: ignore[no-untyped-def]
        available, reason = self.available()
        if not available:
            raise BackendUnavailable(f"container backend unusable: {reason}")

        # An env file rather than repeated -e flags: `docker inspect` and the
        # process list both show -e values to any user on the host.
        env_file = run_dir / f"{step.id}.env"
        atomic_write_bytes(
            env_file,
            "".join(f"{k}={v}\n" for k, v in sorted(env.items()) if "\n" not in v).encode("utf-8"),
            mode=0o600,
        )

        container_workdir = "/workspace"
        rel_cwd = "" if step.cwd in ("", ".") else step.cwd.strip("/")
        if rel_cwd:
            # Confine before interpolating into the container path: `cwd` comes from
            # a plan file, which is data.
            resolve_within(workdir, rel_cwd)
        container_cwd = f"{container_workdir}/{rel_cwd}" if rel_cwd else container_workdir

        argv = [
            self.runtime,
            "run",
            "--rm",
            "--cap-drop=ALL",
            "--security-opt=no-new-privileges",
            "--read-only",
            f"--user={os.getuid()}:{os.getgid()}",
            f"--pids-limit={limits.processes}",
            f"--memory={limits.memory_mb}m",
            f"--memory-swap={limits.memory_mb}m",
            f"--cpus={limits.cpus:g}",
            "--tmpfs=/tmp:rw,noexec,nosuid,size=128m",
            f"--volume={workdir.resolve()}:{container_workdir}:rw",
            f"--workdir={container_cwd}",
            f"--env-file={env_file}",
            f"--env=HOME={container_workdir}/.harness-home",
            "--env=TMPDIR=/tmp",
        ]
        argv.append("--network=host" if step.allow_network else "--network=none")
        argv += [self.image, *step.run]

        stdout_path = run_dir / f"{step.id}.stdout"
        stderr_path = run_dir / f"{step.id}.stderr"
        wall = step.timeout_seconds or limits.wall_seconds
        ensure_dir(workdir / ".harness-home")

        started = time.monotonic()
        timed_out = False
        with open(stdout_path, "wb") as out, open(stderr_path, "wb") as err:
            process = subprocess.Popen(  # noqa: S603
                argv,
                cwd=workdir,
                stdout=out,
                stderr=err,
                stdin=subprocess.DEVNULL,
                start_new_session=True,
                close_fds=True,
            )
            try:
                exit_code = process.wait(timeout=wall)
            except subprocess.TimeoutExpired:
                timed_out = True
                exit_code = _terminate_group(process)
        duration_ms = int((time.monotonic() - started) * 1000)
        env_file.unlink(missing_ok=True)

        stdout, stderr, truncated, redactions = _collect_output(stdout_path, stderr_path, limits)
        result = RawResult(
            exit_code=exit_code,
            duration_ms=duration_ms,
            stdout=stdout,
            stderr=stderr,
            truncated=truncated,
            timed_out=timed_out,
            redactions=redactions,
            isolation=self.isolation(step, limits),
        )
        if timed_out:
            raise StepTimeout(f"step {step.id!r} exceeded its {wall:g}s wall clock and was killed")
        return result


def select_sandbox(backend: str, image: str) -> tuple[Sandbox, str]:
    """Resolve the configured backend to a concrete one, and say what happened.

    `auto` is the only value that may fall back, and even then the returned note is
    recorded verbatim in the ledger. Asking for `container` on a machine without one
    is an error: silently running an untrusted step on the host because Docker was
    missing is precisely the substitution this pillar exists to prevent.
    """
    if backend == "local":
        return LocalSandbox(), "configured: local"
    container = ContainerSandbox(image)
    if backend == "container":
        available, reason = container.available()
        if not available:
            raise BackendUnavailable(
                f"execution.backend is 'container' but {reason}",
                hint='set execution.backend to "auto" to permit a recorded fallback to local',
            )
        return container, f"configured: container ({reason})"
    if backend != "auto":
        raise UsageError(f"unknown execution.backend {backend!r}: expected auto, container or local")
    available, reason = container.available()
    if available:
        return container, f"auto: container ({reason})"
    return LocalSandbox(), f"auto: local — container unavailable ({reason})"


# --------------------------------------------------------------------------- #
# Output handling
# --------------------------------------------------------------------------- #

def _terminate_group(process: subprocess.Popen[bytes]) -> int:
    """SIGTERM the session, then SIGKILL what is left.

    Killing the process group and not just the child is the difference between a
    timeout and a leaked `make -j` that keeps eating the runner after the harness
    has moved on.
    """
    try:
        pgid = os.getpgid(process.pid)
    except ProcessLookupError:
        return process.poll() or -signal.SIGKILL
    for sig, grace in ((signal.SIGTERM, 5.0), (signal.SIGKILL, 5.0)):
        try:
            os.killpg(pgid, sig)
        except ProcessLookupError:
            break
        try:
            return process.wait(timeout=grace)
        except subprocess.TimeoutExpired:
            continue
    return -signal.SIGKILL


def _read_capped(path: Path, limit: int) -> tuple[str, bool]:
    """Read a log, keeping the head and the tail when it is too long.

    Both ends, because the head has the command and the tail has the error. Decoded
    with `errors="replace"`: a step is free to emit invalid UTF-8, and a harness
    that crashes while reporting a failure is worse than one that prints U+FFFD.
    """
    size = path.stat().st_size if path.exists() else 0
    if size <= limit:
        return (path.read_bytes().decode("utf-8", errors="replace") if size else ""), False
    half = limit // 2
    with open(path, "rb") as handle:
        head = handle.read(half)
        handle.seek(size - half)
        tail = handle.read(half)
    notice = TRUNCATION_NOTICE.format(dropped=size - 2 * half)
    return (
        head.decode("utf-8", errors="replace") + notice + tail.decode("utf-8", errors="replace"),
        True,
    )


def _collect_output(stdout_path: Path, stderr_path: Path, limits: Limits) -> tuple[str, str, bool, list[str]]:
    out_text, out_trunc = _read_capped(stdout_path, limits.output_bytes)
    err_text, err_trunc = _read_capped(stderr_path, limits.output_bytes)
    # Scrub before anything else touches these strings. From here on they are
    # written to the run folder, hashed into the artifact store, and summarised in
    # the ledger; there is no later point at which redaction still helps.
    out_clean, out_hits = scrub(out_text)
    err_clean, err_hits = scrub(err_text)
    atomic_write_bytes(stdout_path, out_clean.encode("utf-8"))
    atomic_write_bytes(stderr_path, err_clean.encode("utf-8"))
    return out_clean, err_clean, out_trunc or err_trunc, sorted(set(out_hits + err_hits))


def collect_outputs(step: Step, workdir: Path) -> list[tuple[Output, Path]]:
    """Expand each declared output glob inside the worktree.

    Sorted, so the artifact set — and therefore the manifest digest — does not
    depend on directory iteration order. A required output that matched nothing is
    left for the artifact store to reject by name, so the error says which output
    was missing rather than "no files matched".
    """
    found: list[tuple[Output, Path]] = []
    base = workdir.resolve()
    for output in sorted(step.outputs, key=lambda o: o.path):
        matches = sorted(globlib.glob(str(base / output.path), recursive=True))
        if not matches and not output.optional:
            found.append((output, base / output.path))
            continue
        for match in matches:
            path = Path(match)
            if path.is_file() and path.resolve().is_relative_to(base):
                found.append((output, path))
    return found


def tool_fingerprints(tools: Iterable[str], *, cwd: Path, env: dict[str, str]) -> dict[str, str]:
    """Run each declared version probe and digest its output.

    Probes run outside the sandbox, on the host that will do the work, because that
    is the toolchain whose identity the cache key needs. A probe that fails is
    recorded as failing rather than skipped: an absent compiler is a different
    cache key from a present one.
    """
    prints: dict[str, str] = {}
    for command in sorted(set(tools)):
        argv = shlex.split(command)
        if not argv:
            continue
        try:
            probe = subprocess.run(  # noqa: S603
                argv, cwd=cwd, env=env, capture_output=True, text=True, timeout=30, errors="replace"
            )
            payload = {"rc": probe.returncode, "out": probe.stdout.strip(), "err": probe.stderr.strip()}
        except (FileNotFoundError, subprocess.TimeoutExpired, PermissionError) as exc:
            payload = {"rc": None, "error": type(exc).__name__}
        prints[command] = digest_json(payload)
    return prints


def describe_command(step: Step) -> str:
    return " ".join(shlex.quote(part) for part in scrub_argv(step.run))


def ledger_body(step: Step, env: dict[str, str]) -> dict[str, Any]:
    """What a STEP_STARTED record should carry: the command and the environment
    contract, both scrubbed, and never a raw environment value."""
    return {
        "step": step.id,
        "command": scrub_argv(list(step.run)),
        "cwd": step.cwd,
        "env_names": sorted(env),
        "env_digest": digest_json(env_fingerprint(env)),
        "env_preview": scrub_env({k: v for k, v in env.items() if k in ("PATH", "HOME", "TZ", "LC_ALL")}),
    }
