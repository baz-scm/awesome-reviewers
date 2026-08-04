"""Pillar 1b — the append-only, hash-chained run ledger.

Git records what the code became. It does not record how it got there: which agent
ran which command, in which sandbox, against which policy version, with which
cache entries reused, and who approved the phase. That is the history this ledger
holds, and it is committed to git so that the record of the process is as durable
as the record of the result.

Three properties, each earned by a specific mechanism:

  append-only    the file is opened `O_APPEND` under an exclusive lock, and no
                 code path in this package rewrites a line
  tamper-evident every record's digest covers the previous record's digest, so
                 editing or deleting record *n* invalidates every record after it
  orderable      records carry a monotonic `seq`; the wall-clock `at` is recorded
                 for humans and never used to order anything

Derived from the corpus:
  cli-use-file-locks (snyk/cli) — use flock for mutual exclusion over a shared
      filesystem resource; the kernel releasing it on process death is the property
      a pid file cannot offer.
  redis-atomic-contracts-enforcement (redis/redis) — an operation that claims to be
      atomic must be atomic at every layer that can observe it.
  apisix-verify-download-integrity (apache/apisix) — fail closed when a digest does
      not match. `verify` reporting the first broken record and refusing to continue
      is that rule applied to a chain.
  aidlc-workflows-single-transaction-locking — reading the tail and appending the
      next record is one transaction. Split them and two writers build two forks
      of the chain from the same predecessor.
  aidlc-workflows-scoped-hash-based-idempotency — do not read completion signals
      from all of history. `since_stage_start` floors every such query at the
      latest STAGE_STARTED for that stage run, so a re-run with the same stage
      name is evaluated on its own evidence.
  aidlc-workflows-no-silent-null-artifacts — a record that cannot be parsed is an
      integrity failure, never an empty result.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any, Iterable, Iterator

from . import SCHEMA_VERSION
from .digest import ZERO, canonical_json, digest_bytes, is_digest, require_digest
from .errors import IntegrityError, UsageError
from .paths import ensure_dir
from .workspace import file_lock, utc_now

LEDGER_NAME = "ledger.jsonl"
LOCK_NAME = "ledger.lock"

# The vocabulary. Closed on purpose: an unknown type in a ledger read back later is
# a schema problem, and the enum is what lets `verify` say so.
RUN_STARTED = "RUN_STARTED"
RUN_FINISHED = "RUN_FINISHED"
STAGE_STARTED = "STAGE_STARTED"
STAGE_FINISHED = "STAGE_FINISHED"
SNAPSHOT_CREATED = "SNAPSHOT_CREATED"
STEP_STARTED = "STEP_STARTED"
STEP_FINISHED = "STEP_FINISHED"
CACHE_HIT = "CACHE_HIT"
CACHE_MISS = "CACHE_MISS"
ARTIFACT_PUBLISHED = "ARTIFACT_PUBLISHED"
GATE_EVALUATED = "GATE_EVALUATED"
POLICY_PACK_BUILT = "POLICY_PACK_BUILT"
ATTESTATION_CREATED = "ATTESTATION_CREATED"
APPROVAL_RECORDED = "APPROVAL_RECORDED"
WAIVER_APPLIED = "WAIVER_APPLIED"

RECORD_TYPES = frozenset(
    {
        RUN_STARTED,
        RUN_FINISHED,
        STAGE_STARTED,
        STAGE_FINISHED,
        SNAPSHOT_CREATED,
        STEP_STARTED,
        STEP_FINISHED,
        CACHE_HIT,
        CACHE_MISS,
        ARTIFACT_PUBLISHED,
        GATE_EVALUATED,
        POLICY_PACK_BUILT,
        ATTESTATION_CREATED,
        APPROVAL_RECORDED,
        WAIVER_APPLIED,
    }
)

# Fields covered by the digest. Listed explicitly so that adding a field to a
# record cannot silently change what the chain commits to.
_SIGNED_FIELDS = ("v", "seq", "at", "run_id", "stage", "type", "body", "prev")


@dataclass(frozen=True)
class Record:
    v: int
    seq: int
    at: str
    run_id: str
    stage: str
    type: str
    body: dict[str, Any]
    prev: str
    digest: str

    @classmethod
    def from_json(cls, raw: dict[str, Any], *, where: str) -> "Record":
        missing = [f for f in (*_SIGNED_FIELDS, "digest") if f not in raw]
        if missing:
            raise IntegrityError(f"{where}: ledger record missing {', '.join(missing)}")
        version = raw["v"]
        if not isinstance(version, int) or version > SCHEMA_VERSION:
            raise IntegrityError(
                f"{where}: ledger record schema {version!r} is newer than this harness "
                f"understands (supports {SCHEMA_VERSION})",
                hint="upgrade awesome-harness; do not rewrite the ledger",
            )
        if not isinstance(raw["body"], dict):
            raise IntegrityError(f"{where}: ledger record body must be an object")
        return cls(
            v=version,
            seq=int(raw["seq"]),
            at=str(raw["at"]),
            run_id=str(raw["run_id"]),
            stage=str(raw["stage"]),
            type=str(raw["type"]),
            body=raw["body"],
            prev=require_digest(raw["prev"], field="prev") if raw["prev"] != ZERO else ZERO,
            digest=require_digest(raw["digest"], field="digest"),
        )

    def payload(self) -> dict[str, Any]:
        return {field: getattr(self, field) for field in _SIGNED_FIELDS}

    def computed_digest(self) -> str:
        return digest_bytes(canonical_json(self.payload()))

    def to_json(self) -> dict[str, Any]:
        return {**self.payload(), "digest": self.digest}

    def summary(self) -> str:
        detail = {
            STAGE_STARTED: lambda b: str(b.get("stage", "")),
            STEP_FINISHED: lambda b: f"{b.get('step', '?')} exit={b.get('exit_code', '?')}",
            CACHE_HIT: lambda b: f"{b.get('step', '?')} key={b.get('key', '')[7:19]}",
            CACHE_MISS: lambda b: f"{b.get('step', '?')} key={b.get('key', '')[7:19]}",
            GATE_EVALUATED: lambda b: f"{b.get('verdict', '?')} findings={b.get('findings', 0)}",
            ARTIFACT_PUBLISHED: lambda b: f"{b.get('name', '?')} {b.get('digest', '')[7:19]}",
            SNAPSHOT_CREATED: lambda b: f"tree={str(b.get('tree', ''))[:12]}",
            ATTESTATION_CREATED: lambda b: f"{b.get('signature', '?')}",
        }.get(self.type)
        tail = f"  {detail(self.body)}" if detail else ""
        return f"{self.seq:>4}  {self.at}  {self.type:<20}{tail}"


@dataclass
class VerifyResult:
    ok: bool
    count: int
    head: str
    broken_at: int | None = None
    reason: str | None = None


class Ledger:
    """The chain. One instance per repository."""

    def __init__(self, directory: Path) -> None:
        self.dir = ensure_dir(directory)
        self.path = self.dir / LEDGER_NAME
        self.lock_path = self.dir / LOCK_NAME

    # ---- writing --------------------------------------------------------- #

    def append(
        self,
        type: str,
        body: dict[str, Any] | None = None,
        *,
        run_id: str = "",
        stage: str = "",
    ) -> Record:
        """Append one record. Reading the tail and writing the successor is atomic.

        The lock spans both halves deliberately. If the tail were read outside it,
        two concurrent steps in the same run would both see record *n* as their
        predecessor and produce two records claiming the same `prev` — a fork that
        `verify` would report but that no amount of later repair could untangle.
        """
        if type not in RECORD_TYPES:
            raise UsageError(f"unknown ledger record type: {type}")
        payload_body = dict(body or {})
        with file_lock(self.lock_path):
            tail = self._read_tail()
            record = Record(
                v=SCHEMA_VERSION,
                seq=(tail.seq + 1) if tail else 1,
                at=utc_now(),
                run_id=run_id,
                stage=stage,
                type=type,
                body=payload_body,
                prev=tail.digest if tail else ZERO,
                digest="",
            )
            record = replace(record, digest=record.computed_digest())
            line = canonical_json(record.to_json()) + b"\n"

            # O_APPEND plus one write call: the record lands whole or not at all,
            # and fsync means a crash after this point cannot lose it.
            fd = os.open(self.path, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o644)
            try:
                os.write(fd, line)
                os.fsync(fd)
            finally:
                os.close(fd)
            return record

    # ---- reading --------------------------------------------------------- #

    def exists(self) -> bool:
        return self.path.is_file() and self.path.stat().st_size > 0

    def _read_tail(self) -> Record | None:
        """Last record, read by seeking from the end rather than parsing the file.

        Called on every append, so it must not be O(file). A torn final line is
        raised rather than skipped: with an fsynced single-write append under lock,
        the only way to get one is genuine corruption or an outside editor.
        """
        if not self.exists():
            return None
        window = 1 << 16
        size = self.path.stat().st_size
        with open(self.path, "rb") as handle:
            while True:
                start = max(0, size - window)
                handle.seek(start)
                chunk = handle.read(size - start)
                lines = [line for line in chunk.split(b"\n") if line.strip()]
                if lines and (start == 0 or len(lines) > 1):
                    break
                if start == 0:
                    return None
                window *= 2
        try:
            raw = json.loads(lines[-1].decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise IntegrityError(
                f"{self.path}: final ledger line is not valid JSON — the chain is truncated "
                f"or was edited by hand ({exc})"
            ) from exc
        return Record.from_json(raw, where=f"{self.path}:tail")

    def read_all(self) -> list[Record]:
        if not self.exists():
            return []
        records: list[Record] = []
        with open(self.path, "r", encoding="utf-8") as handle:
            for number, line in enumerate(handle, start=1):
                if not line.strip():
                    continue
                try:
                    raw = json.loads(line)
                except json.JSONDecodeError as exc:
                    raise IntegrityError(f"{self.path}:{number}: invalid JSON: {exc.msg}") from exc
                records.append(Record.from_json(raw, where=f"{self.path}:{number}"))
        return records

    def head(self) -> str:
        tail = self._read_tail()
        return tail.digest if tail else ZERO

    def verify(self) -> VerifyResult:
        """Recompute the whole chain.

        Checks four things per record: the digest matches its own contents, `prev`
        matches the actual predecessor, `seq` increments by exactly one, and the
        type is known. Any one of them failing localises the tampering to a
        sequence number.
        """
        records = self.read_all()
        expected_prev = ZERO
        expected_seq = 1
        for record in records:
            if record.seq != expected_seq:
                return VerifyResult(
                    False,
                    len(records),
                    expected_prev,
                    record.seq,
                    f"sequence jumped: expected {expected_seq}, found {record.seq} "
                    f"(a record was removed or inserted)",
                )
            if record.prev != expected_prev:
                return VerifyResult(
                    False,
                    len(records),
                    expected_prev,
                    record.seq,
                    f"broken link: record {record.seq} points at {record.prev[:19]} "
                    f"but its predecessor hashes to {expected_prev[:19]}",
                )
            recomputed = record.computed_digest()
            if recomputed != record.digest:
                return VerifyResult(
                    False,
                    len(records),
                    expected_prev,
                    record.seq,
                    f"record {record.seq} was modified: contents hash to {recomputed[:19]}, "
                    f"record claims {record.digest[:19]}",
                )
            if record.type not in RECORD_TYPES:
                return VerifyResult(
                    False, len(records), expected_prev, record.seq, f"unknown type {record.type!r}"
                )
            expected_prev = record.digest
            expected_seq += 1
        return VerifyResult(True, len(records), expected_prev)

    # ---- queries --------------------------------------------------------- #

    def iter_run(self, run_id: str) -> Iterator[Record]:
        for record in self.read_all():
            if record.run_id == run_id:
                yield record

    def since_stage_start(
        self,
        run_id: str,
        stage: str,
        types: Iterable[str] | None = None,
    ) -> list[Record]:
        """Records emitted after the *latest* STAGE_STARTED for this run and stage.

        This is the query that makes re-entry correct. An append-only ledger keeps
        every previous attempt, so "has this stage converged?" answered over all of
        history says yes on the strength of a run that happened yesterday against
        different code. Flooring at the current stage-run boundary means a re-run is
        judged on its own records — and, equally, that a stage which genuinely did
        converge in this run is not made to repeat itself.
        """
        wanted = set(types) if types else None
        records = self.read_all()
        floor = 0
        for record in records:
            if record.type == STAGE_STARTED and record.run_id == run_id and record.stage == stage:
                floor = record.seq
        out: list[Record] = []
        for record in records:
            if record.seq <= floor or record.run_id != run_id or record.stage != stage:
                continue
            if wanted and record.type not in wanted:
                continue
            out.append(record)
        return out

    def last(self, type: str, *, run_id: str | None = None) -> Record | None:
        found = None
        for record in self.read_all():
            if record.type == type and (run_id is None or record.run_id == run_id):
                found = record
        return found

    def runs(self) -> list[dict[str, Any]]:
        """One row per run, newest last, for `awesome-harness ledger runs`."""
        rows: dict[str, dict[str, Any]] = {}
        for record in self.read_all():
            if not record.run_id:
                continue
            row = rows.setdefault(
                record.run_id,
                {"run_id": record.run_id, "started": record.at, "records": 0, "verdict": None},
            )
            row["records"] += 1
            row["finished"] = record.at
            if record.type == GATE_EVALUATED:
                row["verdict"] = record.body.get("verdict")
            if record.type == RUN_FINISHED:
                row["status"] = record.body.get("status")
        return list(rows.values())


def head_or_zero(ledger: Ledger) -> str:
    head = ledger.head()
    return head if is_digest(head) else ZERO
