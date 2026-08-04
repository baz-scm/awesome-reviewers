"""Pillar 4 — reuse of deterministic work.

A cache is a claim that two executions would have produced the same result. The
claim is only as good as the key, so this module is mostly about the key: what goes
in it, what must stay out of it, what happens when two different input sets land on
one key, and how to explain a miss to whoever is waiting for it.

**What is in the key.** The step's identity (argv, cwd, declared env, output paths,
network flag), the digest of every declared input file, a fingerprint of every
declared tool version, a digest per environment value the step will see, the policy
pack digest, the platform, the resolved isolation backend, and the harness schema
and version.

**What is deliberately not.** The run id, any timestamp, the actor, the ledger head,
the hostname, absolute paths, the cache directory, and the git commit sha. Each of
those changes between two runs that *should* hit, so including any one of them
would produce a cache with a permanent 0% hit rate — the failure mode that looks
like a working cache right up until someone measures it.

**Under-declared inputs.** A step that declares no inputs cannot be cached, and
says so, rather than being cached against nothing and hitting forever. This is the
one place the harness refuses to guess: a wrong `inputs` list is a stale build, and
a stale build is indistinguishable from a correct one until it ships.

Derived from the corpus:
  aidlc-workflows-scoped-hash-based-idempotency — key by content, not identity;
      detect same-key conflicts and fail loudly rather than keeping the first; and
      scope completion signals to the current run window. That last part is why
      *content* reuse lives here and *convergence* lives in the ledger:
      content-addressed reuse across runs is the point, whereas a "this stage
      already finished" signal read from all of history is a bug.
  aidlc-workflows-no-silent-null-artifacts — a hit whose blobs have been evicted is
      a miss, not an empty result.
  aidlc-workflows-fail-loudly-degrade-safely — a corrupt entry is deleted and
      reported, never partially trusted.
"""

from __future__ import annotations

import json
import platform as platform_mod
import sys
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from . import SCHEMA_VERSION, __version__
from .artifacts import Artifact, Store
from .digest import digest_json, hex_of, require_digest
from .errors import CacheCollision, ConfigError, IntegrityError
from .execution import Limits, Step
from .paths import ensure_dir
from .workspace import atomic_write_json, read_json, utc_now


# Environment variables whose *values* are per-run by construction: HOME is pointed
# at the run folder for isolation, TMPDIR follows it. Their names still belong in the
# key — a step that suddenly sees HOME is a different step — but their values must
# not, or every run would compute a fresh key and the cache would never hit while
# looking, from the outside, exactly like a cache that works.
RUN_SCOPED_ENV = frozenset({"HOME", "TMPDIR", "TMP", "TEMP", "PWD", "OLDPWD"})
RUN_SCOPED_MARKER = "run-scoped"


def platform_identity() -> dict[str, str]:
    """The parts of the machine that change results, and none of the parts that do not.

    `system`, `machine` and the Python minor version: a wheel built on aarch64 is
    not the artifact x86_64 needs. Explicitly absent: hostname, kernel release, cpu
    count and load — a cache keyed on the kernel patch level is a cache that empties
    itself on every unattended upgrade.
    """
    return {
        "system": platform_mod.system(),
        "machine": platform_mod.machine(),
        "python": f"{sys.version_info.major}.{sys.version_info.minor}",
    }


@dataclass(frozen=True)
class KeyInputs:
    """Everything the key commits to, kept as data so a miss can be explained."""

    schema: int
    harness: str
    step: dict[str, Any]
    inputs: dict[str, str]
    tools: dict[str, str]
    env: dict[str, str]
    policy_pack: str
    platform: dict[str, str]
    isolation: dict[str, Any]

    def key(self) -> str:
        return digest_json(asdict(self))

    def to_json(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_json(cls, raw: dict[str, Any]) -> "KeyInputs":
        return cls(
            schema=int(raw.get("schema", SCHEMA_VERSION)),
            harness=str(raw.get("harness", "")),
            step=dict(raw.get("step") or {}),
            inputs=dict(raw.get("inputs") or {}),
            tools=dict(raw.get("tools") or {}),
            env=dict(raw.get("env") or {}),
            policy_pack=str(raw.get("policy_pack", "")),
            platform=dict(raw.get("platform") or {}),
            isolation=dict(raw.get("isolation") or {}),
        )

    def differences(self, other: "KeyInputs") -> list[str]:
        """Human-readable field-by-field diff. This is the miss explanation."""
        notes: list[str] = []
        if self.harness != other.harness:
            notes.append(f"harness version {other.harness} -> {self.harness}")
        if self.schema != other.schema:
            notes.append(f"schema {other.schema} -> {self.schema}")
        if self.step != other.step:
            for field_name in sorted(set(self.step) | set(other.step)):
                if self.step.get(field_name) != other.step.get(field_name):
                    notes.append(f"step.{field_name} changed")
        for label, mine, theirs in (
            ("input", self.inputs, other.inputs),
            ("tool", self.tools, other.tools),
            ("env", self.env, other.env),
        ):
            for name in sorted(set(mine) | set(theirs)):
                if mine.get(name) != theirs.get(name):
                    if name not in theirs:
                        notes.append(f"{label} {name} is new")
                    elif name not in mine:
                        notes.append(f"{label} {name} was removed")
                    else:
                        notes.append(f"{label} {name} changed")
        if self.policy_pack != other.policy_pack:
            notes.append("policy pack changed")
        if self.platform != other.platform:
            notes.append(f"platform {other.platform} -> {self.platform}")
        if self.isolation != other.isolation:
            notes.append(f"isolation {other.isolation} -> {self.isolation}")
        return notes


def isolation_identity(isolation: dict[str, Any]) -> dict[str, Any]:
    """The parts of the sandbox that change a step's result.

    For a container that is the image *digest*, never the tag: a tag is a mutable
    pointer, and a cache keyed on `python:3.11-slim` quietly spans every toolchain
    that tag ever addressed. When no digest is resolvable the tag is recorded under
    a different field name so it can never be mistaken for one.
    """
    backend = str(isolation.get("backend", "unknown"))
    if backend != "container":
        return {"backend": backend}
    digest = isolation.get("image_digest")
    if digest:
        return {"backend": backend, "image_digest": str(digest)}
    return {"backend": backend, "unpinned_image": str(isolation.get("image", "?"))}


@dataclass
class Entry:
    key: str
    step: str
    exit_code: int
    duration_ms: int = 0
    outputs: list[Artifact] = field(default_factory=list)
    stdout_digest: str | None = None
    stderr_digest: str | None = None
    backend: str = "unknown"
    created: str = field(default_factory=utc_now)
    key_inputs: dict[str, Any] = field(default_factory=dict)
    schema: int = SCHEMA_VERSION

    def to_json(self) -> dict[str, Any]:
        return {
            "schema": self.schema,
            "key": self.key,
            "step": self.step,
            "exit_code": self.exit_code,
            "duration_ms": self.duration_ms,
            "outputs": [a.to_json() for a in self.outputs],
            "stdout_digest": self.stdout_digest,
            "stderr_digest": self.stderr_digest,
            "backend": self.backend,
            "created": self.created,
            "key_inputs": self.key_inputs,
        }

    @classmethod
    def from_json(cls, raw: dict[str, Any]) -> "Entry":
        schema = raw.get("schema", SCHEMA_VERSION)
        if not isinstance(schema, int) or schema > SCHEMA_VERSION:
            raise IntegrityError(f"cache entry schema {schema!r} is newer than this harness understands")
        return cls(
            key=require_digest(raw["key"], field="cache key"),
            step=str(raw.get("step", "")),
            exit_code=int(raw.get("exit_code", 0)),
            duration_ms=int(raw.get("duration_ms", 0)),
            outputs=[Artifact.from_json(a) for a in raw.get("outputs", [])],
            stdout_digest=raw.get("stdout_digest"),
            stderr_digest=raw.get("stderr_digest"),
            backend=str(raw.get("backend", "unknown")),
            created=str(raw.get("created", "")),
            key_inputs=dict(raw.get("key_inputs") or {}),
            schema=schema,
        )


@dataclass
class Lookup:
    """The outcome of consulting the cache — hit, miss, or ineligible."""

    key: str
    entry: Entry | None
    eligible: bool
    reason: str
    explanation: list[str] = field(default_factory=list)

    @property
    def hit(self) -> bool:
        return self.entry is not None


class Cache:
    def __init__(self, root: Path, store: Store, *, enabled: bool = True, store_failures: bool = False) -> None:
        self.root = ensure_dir(root)
        self.store = store
        self.enabled = enabled
        # Caching a failure means a flaky test fails identically forever. Off by
        # default; a step that legitimately asserts a nonzero exit should say so.
        self.store_failures = store_failures

    # ---- paths ----------------------------------------------------------- #

    def entry_path(self, key: str) -> Path:
        hexpart = hex_of(require_digest(key, field="cache key"))
        return self.root / "entries" / hexpart[:2] / f"{hexpart[2:]}.json"

    def last_key_path(self, step_id: str) -> Path:
        # Named by digest so an arbitrary step id cannot become a path.
        return self.root / "steps" / f"{hex_of(digest_json(step_id))[:32]}.json"

    # ---- keys ------------------------------------------------------------ #

    @staticmethod
    def eligibility(step: Step) -> tuple[bool, str]:
        if not step.cacheable:
            return False, "step declares cacheable: false"
        if not step.inputs:
            # The refusal that matters. Without declared inputs the key cannot
            # observe the code, so the first result would be reused forever.
            return False, "step declares no inputs, so its result cannot be keyed to content"
        if step.allow_network:
            return False, "step allows network access, so its result is not a function of its inputs"
        return True, "eligible"

    def key_inputs(
        self,
        step: Step,
        *,
        input_digests: dict[str, str],
        tool_digests: dict[str, str],
        env_digests: dict[str, str],
        policy_pack_digest: str,
        isolation: dict[str, Any],
    ) -> KeyInputs:
        return KeyInputs(
            schema=SCHEMA_VERSION,
            harness=__version__,
            step=step.identity(),
            inputs=dict(sorted(input_digests.items())),
            tools=dict(sorted(tool_digests.items())),
            env={
                name: (RUN_SCOPED_MARKER if name in RUN_SCOPED_ENV else digest)
                for name, digest in sorted(env_digests.items())
            },
            policy_pack=policy_pack_digest,
            platform=platform_identity(),
            isolation=isolation_identity(isolation),
        )

    # ---- lookup ---------------------------------------------------------- #

    def lookup(self, step: Step, key_inputs: KeyInputs) -> Lookup:
        key = key_inputs.key()
        eligible, reason = self.eligibility(step)
        if not self.enabled:
            return Lookup(key, None, False, "cache disabled")
        if not eligible:
            return Lookup(key, None, False, reason)

        path = self.entry_path(key)
        if not path.is_file():
            return Lookup(key, None, True, "miss", self._explain(step, key_inputs))

        try:
            entry = Entry.from_json(read_json(path, what="cache entry"))
        except (IntegrityError, ConfigError, KeyError, TypeError, ValueError) as exc:
            # A malformed entry is removed and reported. Leaving it would turn one bad
            # write into a permanent miss with a confusing error every time. The
            # except list is explicit: a bug in this module should surface as a
            # traceback, not be swallowed as "cache was unreadable".
            path.unlink(missing_ok=True)
            return Lookup(key, None, True, f"discarded unreadable cache entry: {exc}")

        # We reached this entry because its path is derived from *our* key. If the
        # inputs it recorded are not ours, then one key addresses two input sets, and
        # returning either side would hand the caller bytes that belong to the other.
        #
        # Comparing the recorded inputs to ours — rather than re-deriving the recorded
        # key and comparing digests — is what makes this reachable. A digest-to-digest
        # comparison can only differ on an actual SHA-256 collision, so it would never
        # catch the cases that really happen: a non-deterministic field creeping into
        # the key function, or an entry written by a build with a different notion of
        # what the key covers.
        recorded = KeyInputs.from_json(entry.key_inputs) if entry.key_inputs else None
        if recorded is not None and asdict(recorded) != asdict(key_inputs):
            raise CacheCollision(
                f"cache key {key[:19]} addresses two different input sets for step {step.id!r}: "
                + "; ".join(key_inputs.differences(recorded)[:5]),
                hint=(
                    "this is a bug in the key function or a corrupted entry, not staleness — "
                    "deleting and retrying would hide it"
                ),
            )

        # A hit whose blobs are gone is a miss. Reporting it as a hit would hand the
        # caller a manifest pointing at nothing.
        missing = [a.name for a in entry.outputs if not self.store.has(a.digest)]
        if missing:
            return Lookup(
                key,
                None,
                True,
                f"entry found but {len(missing)} output blob(s) evicted: {', '.join(missing[:3])}",
            )
        return Lookup(key, entry, True, "hit")

    def _explain(self, step: Step, key_inputs: KeyInputs) -> list[str]:
        """Diff this key against the last key recorded for the same step."""
        path = self.last_key_path(step.id)
        if not path.is_file():
            return ["no previous run of this step is recorded"]
        try:
            previous = KeyInputs.from_json(read_json(path, what="last cache key")["key_inputs"])
        except (ConfigError, IntegrityError, KeyError, TypeError, ValueError):
            return ["previous key for this step could not be read"]
        return key_inputs.differences(previous) or ["key inputs are identical but no entry exists (pruned?)"]

    # ---- store ----------------------------------------------------------- #

    def save(self, entry: Entry, key_inputs: KeyInputs) -> bool:
        """Persist an entry. Returns whether it was actually stored."""
        if not self.enabled:
            return False
        if entry.exit_code != 0 and not self.store_failures:
            return False
        entry.key_inputs = key_inputs.to_json()
        atomic_write_json(self.entry_path(entry.key), entry.to_json())
        atomic_write_json(
            self.last_key_path(entry.step),
            {"step": entry.step, "key": entry.key, "at": utc_now(), "key_inputs": key_inputs.to_json()},
        )
        return True

    def record_key(self, step_id: str, key_inputs: KeyInputs, key: str) -> None:
        """Record the key even for an ineligible step, so the next miss can be explained."""
        atomic_write_json(
            self.last_key_path(step_id),
            {"step": step_id, "key": key, "at": utc_now(), "key_inputs": key_inputs.to_json()},
        )

    # ---- housekeeping ---------------------------------------------------- #

    def entries(self) -> list[Path]:
        base = self.root / "entries"
        return sorted(base.rglob("*.json")) if base.is_dir() else []

    def stats(self) -> dict[str, Any]:
        paths = self.entries()
        return {
            "entries": len(paths),
            "bytes": sum(p.stat().st_size for p in paths),
            "enabled": self.enabled,
        }

    def prune(self, *, max_age_days: float | None = None, dry_run: bool = True) -> tuple[int, int]:
        """Drop entries older than `max_age_days`. Blobs are left to `artifacts gc`.

        Two steps rather than one, because a blob can be referenced by a manifest as
        well as by a cache entry, and only the artifact store knows about all
        references. A prune that also deleted blobs would corrupt manifests.
        """
        cutoff = time.time() - (max_age_days * 86400) if max_age_days else None
        removed = 0
        freed = 0
        for path in self.entries():
            if cutoff is not None and path.stat().st_mtime >= cutoff:
                continue
            freed += path.stat().st_size
            removed += 1
            if not dry_run:
                path.unlink(missing_ok=True)
        return removed, freed

    def referenced_digests(self) -> set[str]:
        """Blob digests any cache entry still points at, for `artifacts gc`."""
        digests: set[str] = set()
        for path in self.entries():
            try:
                raw = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                continue
            for artifact in raw.get("outputs", []):
                if isinstance(artifact, dict) and artifact.get("digest"):
                    digests.add(str(artifact["digest"]))
            for field_name in ("stdout_digest", "stderr_digest"):
                if raw.get(field_name):
                    digests.add(str(raw[field_name]))
        return digests


def limits_from_config(config: dict[str, Any]) -> Limits:
    execution = config.get("execution", {}) if isinstance(config, dict) else {}
    return Limits(
        memory_mb=int(execution.get("memory_mb", 2048)),
        cpu_seconds=int(execution.get("cpu_seconds", 600)),
        cpus=float(execution.get("cpus", 2.0)),
        output_bytes=int(execution.get("output_bytes", 8 << 20)),
        wall_seconds=float(execution.get("timeout_seconds", 900)),
    )
