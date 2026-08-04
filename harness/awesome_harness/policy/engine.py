"""Pillar 6e — gate evaluation and the advisory context bundle.

Blocking by default. A finding at or above the pack's threshold fails the gate, and
softening that is an explicit, recorded choice (`--advisory-only`), not a default.

Two outputs, and they must not be confused:

  **the verdict** — evidence. What the machine decided, over which files, against
  which pack digest, with which findings.

  **the context bundle** — an input. The advisory instructions matching the changed
  files, rendered as markdown for whoever reviews next, human or agent. It proves
  nothing about the code; it is the expertise being delivered to the reviewer.

Waivers are path-scoped, must carry a reason, and expire. An expired waiver stops
suppressing and is reported — a permanent exemption is a policy change, and should
have to look like one.

Derived from the corpus:
  aidlc-workflows-fail-loudly-degrade-safely — if the bundle is capped, say what
      was dropped. A silent truncation reads as "these were all the rules".
  aidlc-workflows-scoped-hash-based-idempotency — scope decisions to the current
      evaluation; a waiver from a previous era is not evidence about this change.
  aidlc-workflows-defensive-observable-error-handling — every unexamined file is
      named in the notes.
"""

from __future__ import annotations

import re
from dataclasses import replace
from datetime import date
from pathlib import Path
from typing import Any, Iterable

from ..errors import ConfigError
from ..scm import Git
from ..workspace import read_json
from .checks import Context, evaluate as run_checks
from .corpus import Corpus
from .findings import (
    ERROR,
    SEVERITIES,
    Finding,
    GateResult,
    Waiver,
    severity_at_least,
)
from .pack import Pack
from .checks import matches_selector

# Caps on the context bundle. Advisory instructions are the product being delivered,
# but a bundle nobody can read is not delivery. Whatever these drop is reported.
MAX_CONTEXT_RULES = 60
MAX_CONTEXT_BYTES = 256 * 1024


class Waivers:
    def __init__(self, entries: list[Waiver]) -> None:
        self.entries = entries

    @classmethod
    def load(cls, path: Path) -> "Waivers":
        if not path.is_file():
            return cls([])
        raw = read_json(path, what="waivers file")
        items = raw.get("waivers", []) if isinstance(raw, dict) else raw
        entries: list[Waiver] = []
        for index, item in enumerate(items or []):
            if not isinstance(item, dict):
                raise ConfigError(f"{path}: waiver {index} is not an object")
            for required in ("check", "path", "reason"):
                if not str(item.get(required, "")).strip():
                    # A waiver without a reason is an unexplained hole in the policy.
                    raise ConfigError(
                        f"{path}: waiver {index} is missing {required!r}",
                        hint="every waiver needs check, path and reason; expires is strongly advised",
                    )
            entries.append(
                Waiver(
                    check=str(item["check"]).strip(),
                    path=str(item["path"]).strip(),
                    reason=str(item["reason"]).strip(),
                    expires=str(item.get("expires", "")).strip(),
                )
            )
        return cls(entries)

    def expired(self, today: str) -> list[Waiver]:
        return [w for w in self.entries if w.expires and w.expires < today]

    def match(self, finding: Finding, today: str) -> str:
        for waiver in self.entries:
            if waiver.check not in (finding.check, "*"):
                continue
            if not matches_selector(finding.path, (waiver.path,)):
                continue
            if waiver.expires and waiver.expires < today:
                continue  # expired: no longer suppresses, and reported separately
            suffix = f" (expires {waiver.expires})" if waiver.expires else " (no expiry set)"
            return f"waiver: {waiver.reason}{suffix}"
        return ""


def build_context(git: Git, root: Path, base: str | None) -> Context:
    """Collect the changed files and their added lines."""
    files = tuple(git.changed_files(base))
    added: dict[str, list[tuple[int, str]]] = {}
    for hunk in git.added_lines(base):
        added.setdefault(hunk.path, []).append((hunk.line, hunk.text))
    return Context(root=root, files=files, added=added)


def evaluate(
    pack: Pack,
    ctx: Context,
    *,
    waivers: Waivers | None = None,
    threshold: str | None = None,
    today: str | None = None,
) -> GateResult:
    """Run the machine tier and decide."""
    effective_threshold = threshold or pack.threshold
    if effective_threshold not in SEVERITIES:
        raise ConfigError(f"threshold must be one of {', '.join(SEVERITIES)}, got {effective_threshold!r}")
    stamp = today or date.today().isoformat()
    waivers = waivers or Waivers([])

    checks = pack.checks()
    findings = run_checks(ctx, checks)

    resolved: list[Finding] = []
    for finding in findings:
        reason = ctx.suppression(finding.path, finding.line, finding.check) or waivers.match(finding, stamp)
        resolved.append(replace(finding, suppressed_by=reason) if reason else finding)

    notes = list(ctx.notes)
    for waiver in waivers.expired(stamp):
        notes.append(
            f"waiver for {waiver.check} on {waiver.path} expired on {waiver.expires} "
            f"and no longer suppresses findings"
        )

    result = GateResult(
        verdict="pass",
        threshold=effective_threshold,
        pack=pack.name,
        pack_digest=pack.digest,
        findings=resolved,
        notes=notes,
        files_examined=len(ctx.files),
        checks_run=len(checks),
    )
    blocking = [
        f for f in resolved if f.blocking and severity_at_least(f.severity, effective_threshold)
    ]
    result.verdict = "fail" if blocking else "pass"
    return result


# Topic relevance. A pack pins every instruction in the corpus, so the bundle has to
# choose, and choosing by discussion volume alone hands a concurrency change a pile of
# naming advice. These map observable features of a diff to the corpus's own topic
# labels: the change tells us which expertise it needs.
TOPIC_SIGNALS: tuple[tuple[str, str], ...] = (
    # Tight on purpose. An earlier draft used `select\\w*` for Database and scored a
    # harness diff at 5,940 — it was matching `selector` and `select_sandbox`. A signal
    # that fires on unrelated identifiers does not merely add noise, it reorders the
    # bundle around a topic the change has nothing to do with.
    ("Concurrency", r"\basync def\b|\bawait |asyncio\.|threading\.|\bThreadPool|\bLock\(|"
                    r"\bmutex\b|sync\.(?:Mutex|RWMutex|WaitGroup)|\bsemaphore\b|"
                    r"concurrent\.futures|\brace condition\b|\bgoroutine\b"),
    ("Error Handling", r"^\s*except\b|^\s*try:|\braise \w|\bthrow new\b|\bcatch\s*\(|"
                       r"^\s*finally:|if err != nil|\.catch\("),
    ("Security", r"\bauth\w*|\btokens?\b|\bsecrets?\b|\bpasswords?\b|\bcredentials?\b|"
                 r"\bsanitiz\w+|\bprivileg\w+|\bencrypt\w*|\bsignatures?\b|\bpermissions?\b|"
                 r"\binjection\b|\btraversal\b"),
    ("Null Handling", r"\bis None\b|\bis not None\b|\bOptional\[|\bnull\b|\bnil\b|"
                      r"\bundefined\b|\bnullable\b|\?\?"),
    ("Configurations", r"os\.environ|\bgetenv\(|\bconfig\w*|\bsettings\b|\.env\b|"
                       r"\bdefaults?\b|\btoml\b"),
    ("Testing", r"\bdef test_|\bassert\w*\s|\bpytest\b|\bunittest\b|\bmock\w*|"
                r"\bfixtures?\b|\bdescribe\(|\bexpect\("),
    ("Logging", r"\blogger\b|\blogging\b|\blog\.\w+\(|console\.\w+\(|\bprint\("),
    ("Performance Optimization", r"\bbenchmark\w*|\blatency\b|\bthroughput\b|\boptimi[sz]\w+|"
                                 r"\bO\(n|\ballocat\w+|\bprofil\w+|\bhot path\b"),
    ("Caching", r"\bcaches?\b|\bcached\b|\bcaching\b|\binvalidat\w+|\bTTL\b|\bmemoi?[sz]\w*"),
    ("Networking", r"\bhttps?\b|requests\.\w+|\bsockets?\b|\btimeouts?\b|\bretr(?:y|ies)\b|"
                   r"\burls?\b|\bendpoints?\b|\btls\b|\bssl\b"),
    ("Database", r"session\.(?:query|scalar|scalars|execute|add|commit)\b|\bsqlalchemy\b|"
                 r"\bcursor\.|\bINSERT INTO\b|\bSELECT\b[^\n]*\bFROM\b|\balembic\b|"
                 r"\bselect\([A-Z]|\.where\(|\.filter_by\(|\btransactions?\b"),
    ("API", r"\binterface \w+|\bexport (?:function|const|class|interface)|@app\.\w+|@router\.|"
            r"\broutes?\b|\bendpoints?\b|\bbackwards? compat\w*"),
    ("CI/CD", r"\bruns-on:|^\s*steps:|^\s*jobs:|\bworkflows?\b|\bpipelines?\b|\bDockerfile\b"),
    ("Observability", r"\bmetrics?\b|\btraces?\b|\bspans?\b|\btelemetry\b|\binstrument\w+|"
                      r"\bprometheus\b|\bopentelemetry\b"),
    ("Migrations", r"\bmigrat\w+|\bschema_version\b|\bbackfill\b|\bdowngrade\b|\balembic\b"),
    ("Documentation", r"\.(?:md|rst)\b|^\s*\"\"\"|\bdocstrings?\b|\bREADME\b"),
)


def change_topics(
    files: Iterable[str], added: dict[str, list[tuple[int, str]]] | None = None
) -> dict[str, int]:
    """Topics the change is about, weighted by how much evidence there is for each.

    Counts rather than a set, and the distinction matters. A large change touches every
    topic at least once — gate a 47-file diff and all fifteen signals fire — so
    membership alone stops discriminating exactly when the corpus is largest and the
    ranking is needed most. Weighting by match count keeps the ordering meaningful at
    any change size, and degrades to "no signal, fall back to specificity" rather than
    to "everything is equally relevant".
    """
    haystack = " ".join(files)
    if added:
        for hunks in added.values():
            haystack += "\n" + "\n".join(text for _, text in hunks)
    weights: dict[str, int] = {}
    for topic, pattern in TOPIC_SIGNALS:
        hits = len(re.findall(pattern, haystack, re.IGNORECASE | re.MULTILINE))
        if hits:
            weights[topic] = hits
    return weights


def advisory_bundle(
    pack: Pack,
    corpus: Corpus,
    changed_files: Iterable[str],
    *,
    max_rules: int = MAX_CONTEXT_RULES,
    max_bytes: int = MAX_CONTEXT_BYTES,
    added: dict[str, list[tuple[int, str]]] | None = None,
) -> tuple[str, list[str], list[str]]:
    """Render the advisory instructions most relevant to this change.

    Returns `(markdown, included_slugs, notes)`. Ranked on three signals, in order:

      1. does its language selector match a changed file, and how specifically — a
         rule scoped to `**/*.py` is about the Python you just wrote, one scoped to
         `**` is general advice and yields to it
      2. does its topic match something the diff actually contains — a change full of
         `await` and `Lock` should surface Concurrency instructions ahead of naming ones
      3. discussion volume, as a tiebreak only

    The pack holds the whole corpus. Without (2) the bundle would rank thousands of
    instructions by popularity and deliver the same generic sixty every time.
    """
    files = list(changed_files)
    notes: list[str] = []
    topics = change_topics(files, added)
    candidates = []
    for rule in pack.advisory_rules:
        matched = [f for f in files if matches_selector(f, rule.selector)]
        if not matched:
            continue
        general = rule.selector == ("**",)
        candidates.append(
            (
                -topics.get(rule.topic, 0),    # topic evidence first, strongest first
                1 if general else 0,           # then selector specificity
                -len(matched),                 # then breadth of match within the change
                rule.slug,
                rule,
            )
        )

    candidates.sort(key=lambda row: row[:4])
    if topics:
        leading = sorted(topics.items(), key=lambda kv: (-kv[1], kv[0]))[:5]
        notes.append(
            "ranked for the topics this change shows most evidence of: "
            + ", ".join(f"{name} ({count})" for name, count in leading)
        )
    included: list[str] = []
    sections: list[str] = []
    size = 0
    dropped_for_count = 0
    dropped_for_size = 0

    for _, _, _, _, rule in candidates:
        if len(included) >= max_rules:
            dropped_for_count += 1
            continue
        instruction = corpus.get(rule.slug)
        section = instruction.as_context()
        if size + len(section) > max_bytes:
            dropped_for_size += 1
            continue
        sections.append(section)
        included.append(rule.slug)
        size += len(section)

    if dropped_for_count:
        notes.append(
            f"{dropped_for_count} advisory instruction(s) omitted from the context bundle: "
            f"rule cap of {max_rules} reached"
        )
    if dropped_for_size:
        notes.append(
            f"{dropped_for_size} advisory instruction(s) omitted from the context bundle: "
            f"byte cap of {max_bytes} reached"
        )

    header = "\n".join(
        [
            f"# Review context — policy pack `{pack.name}`",
            "",
            f"Pack digest: `{pack.digest}`",
            f"Instructions: {len(included)} of {len(pack.advisory_rules)} advisory rules matched "
            f"{len(files)} changed file(s).",
            "",
            "These are distilled from code review discussions in production repositories "
            "(https://awesomereviewers.com). They are review context, not a verdict: the machine "
            "tier of this pack has already run and is reported separately.",
            "",
            "---",
            "",
        ]
    )
    return header + "\n---\n\n".join(sections), included, notes


def render_gate(result: GateResult, *, verbose: bool = False) -> str:
    """Human-readable gate report. Findings first, summary last."""
    lines: list[str] = []
    for finding in result.findings:
        if finding.blocking or verbose:
            lines.append(finding.render())
    if lines:
        lines.append("")
    counts = result.counts
    lines.append(
        f"{result.verdict.upper()}  pack={result.pack} digest={result.pack_digest[7:19]} "
        f"threshold={result.threshold}"
    )
    lines.append(
        f"  {counts.get(ERROR, 0)} error, {counts.get('warning', 0)} warning, "
        f"{counts.get('info', 0)} info across {result.files_examined} changed file(s); "
        f"{result.checks_run} check(s) run"
    )
    suppressed = [f for f in result.findings if not f.blocking]
    if suppressed:
        lines.append(f"  {len(suppressed)} finding(s) suppressed by waiver or inline allow")
    for note in result.notes:
        lines.append(f"  note: {note}")
    return "\n".join(lines)


def summary(result: GateResult) -> dict[str, Any]:
    """The compact form recorded in the ledger and the attestation.

    `blocking` applies the severity threshold; `unsuppressed` does not. Keeping them
    as separate numbers matters: reporting an unsuppressed-warning count under the
    name "blocking" produced the self-contradiction "pass — 3 blocking findings",
    and a gate whose own summary disagrees with its verdict does not get believed.
    """
    return {
        "verdict": result.verdict,
        "blocking": len(result.blocking),
        "unsuppressed": len([f for f in result.findings if f.blocking]),
        "total": len(result.findings),
        "findings_digest": result.findings_digest,
        "pack": result.pack,
        "pack_digest": result.pack_digest,
        "threshold": result.threshold,
    }
