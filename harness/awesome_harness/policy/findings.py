"""Pillar 6b — the finding record.

A gate is only useful if two runs can be compared: which findings are new, which
were fixed, which are the same ones a human already waived. That needs a stable
identity per finding, and a line number is not one — inserting an import above a
violation must not present it as a new violation.

So a fingerprint covers the check, the file, and the normalized offending text, and
excludes the line number. Moving code does not create findings; changing it does.

Derived from the corpus:
  aidlc-workflows-use-scoped-consistent-names — one identifier shape, scoped to
      what it identifies, used everywhere.
  aidlc-workflows-defensive-observable-error-handling — a finding names the input
      that caused it and what to do instead.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any

from ..digest import digest_json
from ..scrub import scrub_text

INFO = "info"
WARNING = "warning"
ERROR = "error"

SEVERITY_ORDER = {INFO: 0, WARNING: 1, ERROR: 2}
SEVERITIES = tuple(SEVERITY_ORDER)

# Inline suppression, e.g. `# harness:allow AH005 - base is a literal prefix`.
# On the offending line or the line immediately above it. A reason is required: an
# unexplained suppression is a finding that was hidden rather than decided.
SUPPRESSION_RE = re.compile(
    r"harness:allow\s+(?P<ids>[A-Z]{2}\d{3}(?:\s*,\s*[A-Z]{2}\d{3})*)\s*(?:[-–:]\s*(?P<reason>.+))?"
)

_WHITESPACE = re.compile(r"\s+")

# Evidence is quoted back to the user and stored in a run artifact, so it is capped
# and scrubbed. 200 characters is enough to recognise a line and short enough that a
# minified bundle cannot flood the report.
EVIDENCE_LIMIT = 200


def normalize_evidence(text: str) -> str:
    return _WHITESPACE.sub(" ", text).strip()


def severity_at_least(severity: str, threshold: str) -> bool:
    return SEVERITY_ORDER.get(severity, 0) >= SEVERITY_ORDER.get(threshold, 2)


@dataclass(frozen=True)
class Finding:
    check: str
    slug: str
    severity: str
    path: str
    line: int
    message: str
    evidence: str = ""
    title: str = ""
    # Set when a waiver or inline suppression matched, with the reason. A suppressed
    # finding is still reported; it just does not block.
    suppressed_by: str = ""

    @property
    def fingerprint(self) -> str:
        """Stable identity across line shifts and whitespace reflows."""
        return digest_json(
            {"check": self.check, "path": self.path, "evidence": normalize_evidence(self.evidence)}
        )

    @property
    def blocking(self) -> bool:
        return not self.suppressed_by

    def to_json(self) -> dict[str, Any]:
        payload = {
            "check": self.check,
            "slug": self.slug,
            "severity": self.severity,
            "path": self.path,
            "line": self.line,
            "message": self.message,
            "evidence": self.evidence,
            "fingerprint": self.fingerprint,
        }
        if self.title:
            payload["title"] = self.title
        if self.suppressed_by:
            payload["suppressed_by"] = self.suppressed_by
        return payload

    def render(self) -> str:
        head = f"{self.path}:{self.line}: {self.severity}[{self.check}] {self.message}"
        parts = [head]
        if self.evidence:
            parts.append(f"    {self.evidence}")
        parts.append(f"    rule: {self.title or self.slug} — https://awesomereviewers.com/reviewers/{self.slug}/")
        if self.suppressed_by:
            parts.append(f"    suppressed: {self.suppressed_by}")
        return "\n".join(parts)


def make_finding(
    *,
    check: str,
    slug: str,
    severity: str,
    path: str,
    line: int,
    message: str,
    evidence: str = "",
    title: str = "",
) -> Finding:
    trimmed = normalize_evidence(evidence)[:EVIDENCE_LIMIT]
    return Finding(
        check=check,
        slug=slug,
        severity=severity,
        path=path,
        line=line,
        message=message,
        # A finding about a hardcoded secret must not quote the secret back into the
        # report, the run folder, and the ledger.
        evidence=scrub_text(trimmed),
        title=title,
    )


@dataclass
class Waiver:
    """A path-scoped, expiring exemption with a stated reason."""

    check: str
    path: str
    reason: str
    expires: str = ""

    def to_json(self) -> dict[str, Any]:
        return {"check": self.check, "path": self.path, "reason": self.reason, "expires": self.expires}


@dataclass
class GateResult:
    verdict: str  # "pass" | "fail"
    threshold: str
    pack: str
    pack_digest: str
    findings: list[Finding] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)
    files_examined: int = 0
    checks_run: int = 0
    advisory_slugs: list[str] = field(default_factory=list)

    @property
    def blocking(self) -> list[Finding]:
        return [f for f in self.findings if f.blocking and severity_at_least(f.severity, self.threshold)]

    @property
    def counts(self) -> dict[str, int]:
        counts = {severity: 0 for severity in SEVERITIES}
        for finding in self.findings:
            counts[finding.severity] = counts.get(finding.severity, 0) + 1
        return counts

    @property
    def findings_digest(self) -> str:
        """Digest over the finding set — what an approval is bound to.

        Sorted fingerprints, so the digest is a function of *which* problems exist
        and not of the order they were discovered. An approval recorded against this
        digest is void the moment the finding set changes, which is the property that
        makes human sign-off meaningful.
        """
        return digest_json(sorted(f.fingerprint for f in self.findings))

    def to_json(self) -> dict[str, Any]:
        return {
            "verdict": self.verdict,
            "threshold": self.threshold,
            "pack": self.pack,
            "pack_digest": self.pack_digest,
            "findings_digest": self.findings_digest,
            "counts": self.counts,
            "blocking": len(self.blocking),
            "files_examined": self.files_examined,
            "checks_run": self.checks_run,
            "advisory_slugs": self.advisory_slugs,
            "findings": [f.to_json() for f in self.findings],
            "notes": self.notes,
        }
