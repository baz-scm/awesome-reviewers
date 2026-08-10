---
title: Sanitize Untrusted Boundaries
description: Treat every externally sourced value (API results, URLs, cached artifacts,
  filesystem-derived error strings, CLI/config inputs) as untrusted at the boundary,
  and apply **context-specific hardening** before it can be rendered, logged, persisted,
  or used in a subprocess.
repository: mvanhorn/last30days-skill
label: Security
language: Python
comments_count: 6
repository_stars: 57799
---

Treat every externally sourced value (API results, URLs, cached artifacts, filesystem-derived error strings, CLI/config inputs) as untrusted at the boundary, and apply **context-specific hardening** before it can be rendered, logged, persisted, or used in a subprocess.

Practical rules:
- **Output encoding/sanitization (context-specific):** If untrusted data may become *active syntax* (Markdown links, HTML, reports), sanitize to an inert form first—e.g., strip embedded newlines and block characters that would corrupt the syntax.
- **Sensitive data minimization:** Never emit absolute local paths (or other environment-specific secrets) in notes/details destined for user-visible reports or internal evidence. Prefer root-relative/basename-only, and when formatting errors, prefer exception class/strerror over raw exception strings that may embed paths.
- **Allowlist/gate propagation:** When propagating cached/derived context (e.g., subreddit context during a drill), only pass it if the current operation’s allowed sources include it.
- **Secure subprocess + auth wiring:** Ensure availability checks use the same auth mode as runtime, and construct subprocess commands defensively (quoting and option terminators like `--` to prevent argument-injection regressions).
- **Destructive actions require explicit ownership signals:** Don’t delete based on filename patterns alone; require a marker in the content/metadata.

Example (Markdown-link hardening):
```py
import re

_SAFE_MARKDOWN_LINK_SCHEMES = ("http://", "https://")
_MARKDOWN_LINK_UNSAFE_CHARS = ("(", ")", "[", "]", "\\")

def _sanitize_url_for_single_line_output(url: str) -> str:
    return re.sub(r"[\r\n]+", " ", url).strip()

def render_untrusted_url(url: str) -> str:
    if not url:
        return ""
    url = _sanitize_url_for_single_line_output(url)
    if not url.startswith(_SAFE_MARKDOWN_LINK_SCHEMES):
        return url  # inert plain text
    if any(ch in url for ch in _MARKDOWN_LINK_UNSAFE_CHARS):
        return url  # inert plain text
    return f"[{url}]({url})"  # safe HTTP(S) only
```

When implementing changes, add regression tests for: delimiter/active-syntax payloads, newline injection, path-leak checks, allowlist gating, and subprocess argument/host edge cases.