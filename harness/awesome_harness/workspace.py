"""On-disk layout, atomic writes, and the one lock everything else takes.

The harness keeps mutable state in four places — the ledger, the artifact store,
the cache, and per-run folders. Three of the six pillars are worthless if a
concurrent writer can interleave with them, and all four are worthless if a
half-written file can be read back as a whole one. Both problems are solved here,
once, rather than in each pillar.

Derived from the corpus:
  cli-use-file-locks (snyk/cli) — when several processes touch the same filesystem
      resource, use flock for mutual exclusion, and put the lock file in a
      directory that already exists rather than inside the one being created.
  clickhouse-consistent-mutex-protection (ClickHouse/ClickHouse) — one lock
      discipline per piece of shared state, applied consistently.
  aidlc-workflows-single-transaction-locking — read-then-append is one
      transaction; take the lock around the pair, not around each half.
  tradingagents-graceful-specific-error-handling (TauricResearch/TradingAgents) —
      when writing persistence, avoid partial or corrupt files by writing to a temp
      path and replacing. That instruction is `atomic_write_bytes` almost verbatim.
  aidlc-workflows-portable-configuration-standards — configuration is data in one
      documented file, not environment archaeology.
  aidlc-workflows-explicit-environment-contracts — the environment a step may see
      is declared, not inherited.
"""

from __future__ import annotations

import errno
import fcntl
import json
import os
import secrets
import time
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator

from . import SCHEMA_VERSION
from .errors import ConfigError, HarnessError, NotInitialized
from .paths import ensure_dir

HARNESS_DIR = ".harness"
CONFIG_NAME = "config.json"

# Committed state. This is the part of the harness that belongs in git, because it
# *is* the durable history: the chain, the pinned policy, and the attestations that
# reference them.
COMMITTED = ("config.json", "policy", "ledger", "attestations", "waivers.json")

# Local state. Reproducible from the committed state plus a re-run, so it is
# gitignored: a 157MB artifact store in git would be a bug, not durability.
LOCAL = ("runs", "artifacts", "cache", "tmp", "snapshots")


DEFAULT_CONFIG: dict[str, Any] = {
    "schema": SCHEMA_VERSION,
    "policy": {
        # Where the Awesome Reviewers corpus lives. A path relative to the repo
        # root when the corpus is vendored (as it is in this repository), else an
        # absolute path or a directory holding a downloaded raw/index.json.
        "corpus": "_reviewers",
        "pack": "default",
        # Findings at or above this severity block. Blocking by default is the
        # point; `--advisory-only` is an explicit, recorded downgrade.
        "threshold": "error",
    },
    "execution": {
        # auto -> container when a container runtime is present, else local. The
        # resolved backend is recorded in the ledger and the attestation, so a
        # local run never reads as a container run.
        "backend": "auto",
        "image": "python:3.11-slim",
        "timeout_seconds": 900,
        "memory_mb": 2048,
        "cpu_seconds": 600,
        "output_bytes": 8 << 20,
        "network": False,
        # The complete set of environment variables a step may see, by name. Values
        # come from the parent environment; anything absent is simply not set.
        "env_allow": ["PATH", "HOME", "LANG", "LC_ALL", "TZ", "TMPDIR"],
        # Deterministic overlay applied on top, after the allowlist.
        "env_fixed": {
            "TZ": "UTC",
            "LC_ALL": "C.UTF-8",
            "LANG": "C.UTF-8",
            "PYTHONHASHSEED": "0",
            "PYTHONDONTWRITEBYTECODE": "1",
            "SOURCE_DATE_EPOCH": "0",
        },
    },
    "cache": {"enabled": True},
    "identity": {
        # "ssh" uses `ssh-keygen -Y sign`. "none" produces an attestation that is
        # explicitly labelled unsigned. There is no third option that fabricates a
        # signature, and an unsigned attestation never verifies as signed.
        "signer": "ssh",
        "key": "",
        "allowed_signers": ".harness/allowed_signers",
        "namespace": "awesome-harness",
    },
    "plan": "harness/plans/default.json",
}


def utc_now() -> str:
    """Wall-clock stamp, second precision, always UTC and always suffixed Z.

    Recorded for humans and for range queries. Never used to order records: the
    ledger orders by its own monotonic sequence number, because two records
    written inside the same second — or across an NTP step — would otherwise be
    unorderable.
    """
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def new_run_id() -> str:
    """Sortable, collision-resistant, and readable in a directory listing."""
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + secrets.token_hex(3)


def atomic_write_bytes(path: Path, data: bytes, *, mode: int = 0o644) -> None:
    """Write via a sibling temp file, fsync, rename, then fsync the directory.

    A reader either sees the previous file or the new one. Without the directory
    fsync the rename itself can be lost on power failure, which for an append-only
    ledger means losing the record that proves the chain.
    """
    ensure_dir(path.parent)
    tmp = path.parent / f".{path.name}.{os.getpid()}.tmp"
    try:
        fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, mode)
        try:
            os.write(fd, data)
            os.fsync(fd)
        finally:
            os.close(fd)
        os.replace(tmp, path)
        dir_fd = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(dir_fd)
        finally:
            os.close(dir_fd)
    except BaseException:
        tmp.unlink(missing_ok=True)
        raise


def atomic_write_json(path: Path, payload: Any) -> None:
    from .digest import canonical_json

    atomic_write_bytes(path, canonical_json(payload) + b"\n")


def read_json(path: Path, *, what: str = "file") -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ConfigError(f"{what} not found: {path}") from exc
    except json.JSONDecodeError as exc:
        # Name the file and the offset. "Expecting value: line 1 column 1" on its
        # own has cost every one of us an afternoon.
        raise ConfigError(f"{what} is not valid JSON: {path}:{exc.lineno}:{exc.colno}: {exc.msg}") from exc


class LockTimeout(HarnessError):
    exit_code = 11
    kind = "lock"


@contextmanager
def file_lock(path: Path, *, timeout: float = 30.0, poll: float = 0.05) -> Iterator[None]:
    """Exclusive advisory lock held for the whole critical section.

    `flock` and not a pid file: the kernel releases it when the process dies, so a
    crashed run cannot wedge the ledger. Non-blocking retries with a deadline
    rather than a blocking acquire, so a stuck holder produces a diagnosable
    timeout instead of a hang.
    """
    ensure_dir(path.parent)
    fd = os.open(path, os.O_RDWR | os.O_CREAT, 0o644)
    deadline = time.monotonic() + timeout
    try:
        while True:
            try:
                fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except OSError as exc:
                if exc.errno not in (errno.EACCES, errno.EAGAIN):
                    raise
                if time.monotonic() >= deadline:
                    raise LockTimeout(
                        f"could not acquire {path} within {timeout:g}s",
                        hint="another awesome-harness process is writing; wait or stop it",
                    ) from exc
                time.sleep(poll)
        try:
            yield
        finally:
            fcntl.flock(fd, fcntl.LOCK_UN)
    finally:
        os.close(fd)


def _merge(base: Any, override: Any) -> Any:
    """Recursive merge so a partial config.json still gets every default.

    Lists replace rather than concatenate: an `env_allow` that appends to the
    default could never *remove* an inherited variable, which is the whole point
    of an allowlist.
    """
    if isinstance(base, dict) and isinstance(override, dict):
        merged = dict(base)
        for key, value in override.items():
            merged[key] = _merge(base.get(key), value) if key in base else value
        return merged
    return override


@dataclass
class Workspace:
    """Resolved paths and configuration for one repository."""

    root: Path
    config: dict[str, Any] = field(default_factory=lambda: json.loads(json.dumps(DEFAULT_CONFIG)))

    # ---- discovery ------------------------------------------------------- #

    @classmethod
    def find_root(cls, start: Path | None = None) -> Path:
        """Nearest ancestor holding `.harness`, else the nearest git root, else cwd."""
        here = (start or Path.cwd()).resolve()
        for candidate in (here, *here.parents):
            if (candidate / HARNESS_DIR).is_dir():
                return candidate
        for candidate in (here, *here.parents):
            if (candidate / ".git").exists():
                return candidate
        return here

    @classmethod
    def open(cls, start: Path | None = None, *, require: bool = True) -> "Workspace":
        root = cls.find_root(start)
        workspace = cls(root=root)
        config_path = root / HARNESS_DIR / CONFIG_NAME
        if config_path.is_file():
            loaded = read_json(config_path, what="harness config")
            if not isinstance(loaded, dict):
                raise ConfigError(f"harness config must be a JSON object: {config_path}")
            schema = loaded.get("schema", SCHEMA_VERSION)
            if not isinstance(schema, int) or schema > SCHEMA_VERSION:
                raise ConfigError(
                    f"config schema {schema!r} is newer than this harness understands "
                    f"(supports {SCHEMA_VERSION})",
                    hint="upgrade awesome-harness rather than editing the schema down",
                )
            workspace.config = _merge(workspace.config, loaded)
        elif require:
            raise NotInitialized(str(root))
        return workspace

    # ---- layout ---------------------------------------------------------- #

    @property
    def dir(self) -> Path:
        return self.root / HARNESS_DIR

    @property
    def config_path(self) -> Path:
        return self.dir / CONFIG_NAME

    @property
    def policy_dir(self) -> Path:
        return self.dir / "policy"

    @property
    def ledger_dir(self) -> Path:
        return self.dir / "ledger"

    @property
    def attestations_dir(self) -> Path:
        return self.dir / "attestations"

    @property
    def runs_dir(self) -> Path:
        return self.dir / "runs"

    @property
    def artifacts_dir(self) -> Path:
        return self.dir / "artifacts"

    @property
    def cache_dir(self) -> Path:
        return self.dir / "cache"

    @property
    def tmp_dir(self) -> Path:
        return self.dir / "tmp"

    @property
    def snapshots_dir(self) -> Path:
        return self.dir / "snapshots"

    @property
    def waivers_path(self) -> Path:
        return self.dir / "waivers.json"

    def run_dir(self, run_id: str) -> Path:
        from .paths import resolve_within

        # run_id can arrive from argv (`--run-id`), so it is confined like any other
        # external path input rather than joined blindly.
        ensure_dir(self.runs_dir)
        return resolve_within(self.runs_dir, run_id)

    def setting(self, path: str, default: Any = None) -> Any:
        """Dotted lookup: `setting("execution.backend")`."""
        node: Any = self.config
        for part in path.split("."):
            if not isinstance(node, dict) or part not in node:
                return default
            node = node[part]
        return node

    def corpus_path(self) -> Path:
        raw = str(self.setting("policy.corpus", "_reviewers"))
        candidate = Path(raw).expanduser()
        return candidate if candidate.is_absolute() else self.root / candidate

    # ---- creation -------------------------------------------------------- #

    def initialize(self, *, corpus: str | None = None) -> list[Path]:
        created: list[Path] = []
        for name in ("policy", "ledger", "attestations", "runs", "artifacts", "cache", "tmp", "snapshots"):
            target = self.dir / name
            if not target.exists():
                ensure_dir(target)
                created.append(target)

        if corpus:
            self.config.setdefault("policy", {})["corpus"] = corpus
        if not self.config_path.exists():
            atomic_write_json(self.config_path, self.config)
            created.append(self.config_path)
        if not self.waivers_path.exists():
            atomic_write_json(self.waivers_path, {"schema": SCHEMA_VERSION, "waivers": []})
            created.append(self.waivers_path)

        gitignore = self.dir / ".gitignore"
        if not gitignore.exists():
            body = "\n".join(
                [
                    "# Local, reproducible state: regenerate by re-running.",
                    "# The committed half of .harness — config, policy packs, the ledger and",
                    "# attestations — is the durable history and must stay in git.",
                    *[f"/{name}/" for name in LOCAL],
                    "",
                ]
            )
            atomic_write_bytes(gitignore, body.encode("utf-8"))
            created.append(gitignore)
        return created
