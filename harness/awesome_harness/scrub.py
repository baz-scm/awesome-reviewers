"""Credential scrubbing.

The harness persists things a normal build throws away: step stdout and stderr
land in the run folder, argv lands in the ledger, environment contracts land in
the cache key, and all three end up inside an attestation that is designed to be
handed to someone else. That turns any secret that leaks into a subprocess's
output into a secret that is now committed, content-addressed, and signed.

So scrubbing happens on the way *in* to storage, not on the way out to a screen.

Derived from the corpus:
  aidlc-workflows-secure-path-confinement — the sandbox is part of the security
      model: scrub credentials from stdout/stderr before returning or logging.
  aidlc-workflows-secret-scan-baselines — a scanner needs a high-confidence tier
      that can block, separate from a broad tier that only redacts.

Two tiers, deliberately:

  HIGH_CONFIDENCE  provider-shaped tokens. Near-zero false positives, so the
                   policy gate may *block* a change on these.
  BROAD            everything above plus generic `secret = ...` assignments and
                   URL userinfo. Used for redaction only, where over-redacting
                   costs a reader some context and under-redacting leaks a key.
"""

from __future__ import annotations

import re
from typing import Iterable, NamedTuple

REDACTION = "[redacted:{label}]"


class Pattern(NamedTuple):
    label: str
    regex: re.Pattern[str]
    # Group holding the sensitive span. 0 means the whole match.
    group: int = 0


def _p(label: str, pattern: str, *, group: int = 0, flags: int = 0) -> Pattern:
    return Pattern(label, re.compile(pattern, flags), group)


# --------------------------------------------------------------------------- #
# High-confidence: shaped like exactly one provider's credential
# --------------------------------------------------------------------------- #

HIGH_CONFIDENCE: tuple[Pattern, ...] = (
    _p("aws-access-key-id", r"\b(?:A3T[A-Z0-9]|AKIA|ASIA|ABIA|ACCA)[0-9A-Z]{16}\b"),
    _p("github-token", r"\bgh[pousr]_[A-Za-z0-9]{36,251}\b"),
    _p("github-pat", r"\bgithub_pat_[A-Za-z0-9_]{22,251}\b"),
    _p("slack-token", r"\bxox[abposr]-[A-Za-z0-9-]{10,}\b"),
    _p("slack-webhook", r"https://hooks\.slack\.com/services/[A-Za-z0-9/+_-]{20,}"),
    _p("google-api-key", r"\bAIza[0-9A-Za-z_-]{35}\b"),
    _p("anthropic-api-key", r"\bsk-ant-[A-Za-z0-9_-]{20,}\b"),
    _p("openai-api-key", r"\bsk-(?:proj-)?[A-Za-z0-9]{32,}\b"),
    _p("stripe-key", r"\b(?:sk|rk)_(?:live|test)_[A-Za-z0-9]{16,}\b"),
    _p("npm-token", r"\bnpm_[A-Za-z0-9]{36}\b"),
    _p("pypi-token", r"\bpypi-[A-Za-z0-9_-]{40,}\b"),
    _p("hugging-face-token", r"\bhf_[A-Za-z0-9]{34,}\b"),
    _p(
        "private-key",
        r"-----BEGIN (?:[A-Z]+ )?PRIVATE KEY(?: BLOCK)?-----[\s\S]{0,8192}?-----END (?:[A-Z]+ )?PRIVATE KEY(?: BLOCK)?-----",
    ),
    _p("jwt", r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b"),
)

# --------------------------------------------------------------------------- #
# Broad: shaped like a credential in context
# --------------------------------------------------------------------------- #

_SECRET_NAME = (
    r"(?:pass(?:word|wd)?|secret|token|api[_-]?key|access[_-]?key|"
    r"private[_-]?key|client[_-]?secret|credentials?|auth)"
)

CONTEXTUAL: tuple[Pattern, ...] = (
    _p(
        "authorization-header",
        r"(?:authorization|proxy-authorization)\s*[:=]\s*(?:bearer|basic|token)\s+([A-Za-z0-9._\-+/=]{8,})",
        group=1,
        flags=re.IGNORECASE,
    ),
    _p(
        "url-credentials",
        r"[a-z][a-z0-9+.\-]*://[^/\s:@]{1,64}:([^/\s@]{1,256})@",
        group=1,
        flags=re.IGNORECASE,
    ),
    _p(
        "generic-secret",
        rf"\b[A-Za-z0-9_.\-]*{_SECRET_NAME}s?\b\s*[:=]\s*[\"']?([^\s\"',;)]{{6,}})[\"']?",
        group=1,
        flags=re.IGNORECASE,
    ),
)

BROAD: tuple[Pattern, ...] = HIGH_CONFIDENCE + CONTEXTUAL

# Values that are documentation, indirection or an already-scrubbed span. Redacting
# these produces noise and, worse, hides the *compliant* pattern from a reader —
# `token = ${CI_TOKEN}` is the thing we want people to write.
_PLACEHOLDER = re.compile(
    r"""^(?:
          \[redacted:[a-z-]+\]        # our own output, so scrubbing is idempotent
        | \$\{[^}]*\}                 # ${VAR}
        | \{\{[^}]*\}\}               # {{ var }}
        | \$[A-Za-z_][A-Za-z0-9_]*    # $VAR
        | %\([^)]*\)s                 # %(var)s
        | <[^>]*>                     # <your-token-here>
        | \*+ | x+ | \.+
        | (?:none|null|nil|true|false|undefined|empty)
        | (?:redacted|placeholder|example|changeme|dummy|sample|fake|test|todo)[\w.\-]*
        | (?:your|my|the)[_\-][\w.\-]*
        )$""",
    re.IGNORECASE | re.VERBOSE,
)


def looks_like_placeholder(value: str) -> bool:
    return bool(_PLACEHOLDER.match(value.strip()))


class Hit(NamedTuple):
    label: str
    start: int
    end: int


def find(text: str, patterns: Iterable[Pattern] = BROAD) -> list[Hit]:
    """Locate credential spans, longest-first, without overlaps.

    Returned rather than counted so the policy check can report a line number and
    the scrubber can replace precise spans.
    """
    hits: list[Hit] = []
    for pattern in patterns:
        for match in pattern.regex.finditer(text):
            start, end = match.span(pattern.group)
            if start < 0 or end <= start:
                continue
            if looks_like_placeholder(match.group(pattern.group)):
                continue
            hits.append(Hit(pattern.label, start, end))

    hits.sort(key=lambda h: (h.start, -(h.end - h.start)))
    kept: list[Hit] = []
    cursor = -1
    for hit in hits:
        if hit.start >= cursor:
            kept.append(hit)
            cursor = hit.end
    return kept


def scrub(text: str, patterns: Iterable[Pattern] = BROAD) -> tuple[str, list[str]]:
    """Return `(scrubbed_text, labels_found)`.

    The labels come back so the caller can record *that* a secret was seen without
    recording the secret — a step whose log was redacted is worth surfacing.
    """
    hits = find(text, patterns)
    if not hits:
        return text, []
    out: list[str] = []
    cursor = 0
    for hit in hits:
        out.append(text[cursor : hit.start])
        out.append(REDACTION.format(label=hit.label))
        cursor = hit.end
    out.append(text[cursor:])
    return "".join(out), [hit.label for hit in hits]


def scrub_text(text: str) -> str:
    return scrub(text)[0]


def scrub_argv(argv: Iterable[str]) -> list[str]:
    """Scrub a command line before it enters the ledger.

    argv is the single most common place a token gets recorded forever, because
    `--token=...` looks harmless while you are typing it.
    """
    return [scrub_text(arg) for arg in argv]


def scrub_env(env: dict[str, str]) -> dict[str, str]:
    """Redact values whose *name* implies a secret, plus any value that trips a
    high-confidence pattern.

    Name-based redaction is the primary rule here: an environment variable called
    `DEPLOY_TOKEN` is a secret whatever its value happens to look like.
    """
    name_re = re.compile(_SECRET_NAME, re.IGNORECASE)
    out: dict[str, str] = {}
    for key, value in env.items():
        if name_re.search(key) and not looks_like_placeholder(value):
            out[key] = REDACTION.format(label="env-secret")
        else:
            out[key] = scrub_text(value)
    return out
