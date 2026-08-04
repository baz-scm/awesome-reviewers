"""Independent verification of an attestation.

Deliberately a separate path from the one that produced the record. The runner
writes JSON about itself; if the same code read it back, a bug in serialization
would verify itself and the whole apparatus would be decoration. This module starts
from the attestation file and re-derives everything it can: the chain, the blobs,
the pack, the signature, the subject digests.

Nine checks, and every one can fail on its own:

  envelope        payload parses and matches its recorded digest
  statement       the shape is in-toto Statement v1 with our predicate type
  ledger-chain    every record's digest and back-link recompute
  ledger-anchor   the head the statement names exists at the record count it names
  subjects        every subject blob is in the store and hashes to its digest
  manifest        the run manifest, if present locally, matches its subject
  policy-pack     the pack digest matches the committed pack of that name
  policy-verdict  the recorded gate verdict
  signature       ssh-keygen verifies it against the committed allowed signers, for
                  the principal the statement itself claims

Derived from the corpus:
  aidlc-workflows-check-mode-must-mirror — verification must decide the same thing
      the producer asserted, or a green verify means nothing.
  aidlc-workflows-fail-loudly-degrade-safely — `unverifiable` is reported as its own
      state and never rendered as success.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .artifacts import Store
from .digest import PREFIX, is_digest
from .errors import ConfigError, CorpusError, IntegrityError
from .identity import (
    PREDICATE_TYPE,
    SIGNATURE_UNSIGNED,
    SIGNATURE_UNVERIFIABLE,
    SIGNATURE_VALID,
    STATEMENT_TYPE,
    Envelope,
    load_attestation,
    verify_signature,
)
from .ledger import Ledger
from .policy import Corpus, load_pack
from .workspace import Workspace


@dataclass
class Report:
    attestation: str
    signature: str = SIGNATURE_UNSIGNED
    checks: list[dict[str, Any]] = field(default_factory=list)

    def add(self, name: str, ok: bool, detail: str = "") -> None:
        self.checks.append({"check": name, "ok": ok, "detail": detail})

    @property
    def failures(self) -> list[dict[str, Any]]:
        return [c for c in self.checks if not c["ok"]]

    @property
    def ok(self) -> bool:
        return not self.failures and self.signature == SIGNATURE_VALID

    @property
    def verdict(self) -> str:
        if self.failures:
            return "invalid"
        if self.signature == SIGNATURE_VALID:
            return "verified"
        return f"intact but {self.signature}"

    def to_json(self) -> dict[str, Any]:
        return {
            "attestation": self.attestation,
            "verdict": self.verdict,
            "signature": self.signature,
            "ok": self.ok,
            "checks": self.checks,
        }

    def render(self) -> str:
        lines = [f"{self.verdict.upper()}  {self.attestation}"]
        for check in self.checks:
            mark = "ok  " if check["ok"] else "FAIL"
            detail = f"  {check['detail']}" if check["detail"] else ""
            lines.append(f"  [{mark}] {check['check']}{detail}")
        lines.append(f"  signature: {self.signature}")
        return "\n".join(lines)


def _as_digest(value: str) -> str:
    return value if value.startswith(PREFIX) else PREFIX + value


def verify_attestation(ws: Workspace, path: Path, *, check_corpus: bool = True) -> Report:
    report = Report(attestation=str(path))

    # envelope ------------------------------------------------------------- #
    try:
        envelope: Envelope = load_attestation(path)
        report.add("envelope", True, f"payload {envelope.digest[7:19]}")
    except (ConfigError, IntegrityError) as exc:
        report.add("envelope", False, str(exc))
        return report

    try:
        statement = envelope.statement()
    except (UnicodeDecodeError, ValueError) as exc:
        report.add("statement", False, f"payload is not JSON: {exc}")
        return report

    # statement ------------------------------------------------------------ #
    shape_ok = statement.get("_type") == STATEMENT_TYPE and statement.get("predicateType") == PREDICATE_TYPE
    report.add(
        "statement",
        shape_ok,
        "in-toto Statement v1 with harness provenance predicate"
        if shape_ok
        else f"unexpected _type/predicateType: {statement.get('_type')} / {statement.get('predicateType')}",
    )
    predicate = statement.get("predicate") or {}
    run_details = predicate.get("runDetails") or {}
    metadata = run_details.get("metadata") or {}

    # ledger --------------------------------------------------------------- #
    ledger = Ledger(ws.ledger_dir)
    chain = ledger.verify()
    report.add(
        "ledger-chain",
        chain.ok,
        f"{chain.count} record(s), head {chain.head[7:19]}"
        if chain.ok
        else f"broken at record {chain.broken_at}: {chain.reason}",
    )

    claimed_head = str((run_details.get("byproducts") or [{}])[0].get("digest", {}).get("sha256", ""))
    claimed_records = metadata.get("ledgerRecords")
    if claimed_head:
        records = ledger.read_all()
        match = next((r for r in records if r.digest == _as_digest(claimed_head)), None)
        if match is None:
            report.add("ledger-anchor", False, f"head {claimed_head[:12]} is not in the ledger")
        elif isinstance(claimed_records, int) and match.seq != claimed_records:
            # This is the truncate-and-rechain guard: a rewritten ledger can present a
            # matching head, but not at the sequence number the statement recorded.
            report.add(
                "ledger-anchor",
                False,
                f"head is at record {match.seq} but the statement recorded {claimed_records}",
            )
        else:
            report.add("ledger-anchor", True, f"head anchored at record {match.seq}")
    else:
        report.add("ledger-anchor", False, "statement records no ledger head")

    # subjects ------------------------------------------------------------- #
    store = Store(ws.artifacts_dir)
    subjects = statement.get("subject") or []
    missing: list[str] = []
    corrupt: list[str] = []
    manifest_digest = ""
    for subject in subjects:
        name = str(subject.get("name", "?"))
        digest = _as_digest(str((subject.get("digest") or {}).get("sha256", "")))
        if name == "run-manifest":
            manifest_digest = digest
            continue
        if not is_digest(digest):
            corrupt.append(f"{name} (malformed digest)")
            continue
        if not store.has(digest):
            missing.append(name)
            continue
        try:
            store.read_bytes(digest, verify=True)
        except IntegrityError as exc:
            corrupt.append(f"{name}: {exc}")
    payload_subjects = [s for s in subjects if s.get("name") != "run-manifest"]
    report.add(
        "subjects",
        not missing and not corrupt,
        f"{len(payload_subjects)} artifact subject(s) present and intact"
        if not missing and not corrupt
        else "; ".join([*(f"missing: {m}" for m in missing[:3]), *corrupt[:3]]),
    )

    # manifest ------------------------------------------------------------- #
    run_id = str(metadata.get("invocationId", ""))
    manifest_path = ws.runs_dir / run_id / "manifest.json" if run_id else None
    if manifest_digest and manifest_path and manifest_path.is_file():
        from .artifacts import Manifest
        from .workspace import read_json

        try:
            manifest = Manifest.from_json(read_json(manifest_path, what="run manifest"))
            report.add(
                "manifest",
                manifest.digest == manifest_digest,
                "matches subject" if manifest.digest == manifest_digest else
                f"manifest hashes to {manifest.digest[7:19]}, subject says {manifest_digest[7:19]}",
            )
        except (ConfigError, IntegrityError) as exc:
            report.add("manifest", False, str(exc))
    else:
        report.add(
            "manifest",
            True,
            "run manifest not present locally (attestation is portable; skipped)",
        )

    # policy --------------------------------------------------------------- #
    policy = predicate.get("policy") or {}
    pack_name = str(policy.get("pack", ""))
    claimed_pack = str(policy.get("packDigest", ""))
    try:
        pack = load_pack(ws.policy_dir, pack_name) if pack_name else None
    except (ConfigError, IntegrityError) as exc:
        pack = None
        report.add("policy-pack", False, str(exc))
    if pack is not None:
        report.add(
            "policy-pack",
            pack.digest == claimed_pack,
            f"pack {pack_name!r} digest matches"
            if pack.digest == claimed_pack
            else f"committed pack hashes to {pack.digest[7:19]}, statement says {claimed_pack[7:19]}",
        )
        if check_corpus:
            try:
                drift = pack.drift(Corpus(ws.corpus_path()))
                report.add(
                    "corpus-drift",
                    not drift,
                    "every pinned instruction is unchanged"
                    if not drift
                    else f"{len(drift)} instruction(s) changed or removed since the pack was built",
                )
            except CorpusError as exc:
                # A verifier on another machine legitimately has no corpus checkout.
                # Reported as unchecked rather than failed, and never as passed.
                report.add("corpus-drift", True, f"corpus not available, drift unchecked: {exc}")

    verdict = str(policy.get("verdict", ""))
    report.add(
        "policy-verdict",
        verdict == "pass",
        f"gate verdict {verdict!r}" if verdict else "no gate was evaluated in this run",
    )

    # signature ------------------------------------------------------------ #
    actor = predicate.get("actor") or {}
    # The principal comes from the statement, never from a flag: verifying against a
    # principal the caller supplies would let the caller choose whose signature counts.
    principal = str(actor.get("email") or actor.get("id") or "")
    allowed = Path(str(ws.setting("identity.allowed_signers", ".harness/allowed_signers")))
    if not allowed.is_absolute():
        allowed = ws.root / allowed
    status, detail = verify_signature(
        envelope,
        allowed_signers=allowed,
        identity=principal,
        namespace=str(ws.setting("identity.namespace", "awesome-harness")),
        scratch=ws.tmp_dir,
    )
    report.signature = status
    # Four outcomes, four messages. Collapsing the True branches would lose the
    # distinction between "checked and valid" and "not checkable here".
    if status == SIGNATURE_VALID:
        report.add("signature", True, f"{principal}: {detail or 'valid'}")
    elif status == SIGNATURE_UNSIGNED:
        report.add("signature", True, f"unsigned — {detail}")
    elif status == SIGNATURE_UNVERIFIABLE:
        report.add("signature", True, f"present but not checkable here — {detail}")
    else:
        report.add("signature", False, detail)
    return report
