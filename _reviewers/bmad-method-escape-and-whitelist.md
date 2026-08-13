---
title: Escape and whitelist
description: 'When rendering HTML (or HTML-like outputs) from structured data, treat
  every field as potentially hostile—even if produced internally.


  Apply two layers:'
repository: bmad-code-org/bmad-method
label: Security
language: Python
comments_count: 1
repository_stars: 51859
---

When rendering HTML (or HTML-like outputs) from structured data, treat every field as potentially hostile—even if produced internally.

Apply two layers:
1) **Escape free-form text** going into HTML content/attributes (e.g., ids, titles, notes, locations, fixes) using the appropriate encoder.
2) **Whitelist constrained dynamic values** that are interpolated into HTML structure (e.g., CSS class names, SVG attributes). Don’t rely on “it’s only class names”—cap them to a fixed set.

Example pattern (Python):
```python
import html

ALLOWED_STATUS = {"pass", "warn", "fail", "n/a"}
ALLOWED_SEVERITY = {"low", "medium", "high", "critical"}

status = (f.get("status") or "n/a").strip().lower()
if status not in ALLOWED_STATUS:
    status = "n/a"

severity = (f.get("severity") or "low").strip().lower()
if severity not in ALLOWED_SEVERITY:
    severity = "low"

status_class = "na" if status == "n/a" else status

fid = html.escape(f.get("id") or "")
title = html.escape(f.get("title") or "")
note = html.escape(f.get("note") or "")

# Only interpolate whitelisted values into HTML structure
article = f'<article class="finding finding-{status_class}">'
``` 

Even for locally-generated reports, keep the allowlist defense-in-depth as a standard when the code constructs HTML tokens (classes/ids/attrs) from input fields.