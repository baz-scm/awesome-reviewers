---
title: Consumer-Ready Documentation
description: 'When writing technical documentation, ensure it is accurate for real
  usage and immediately actionable for the reader (human or script). In practice:


  - Flag exceptions explicitly (“caveats”): If behavior depends on provider/platform/version
  (e.g., hooks not running for some providers), include a clearly visible caveat section
  describing the affected cases...'
repository: cline/cline#v1
label: Documentation
language: Other
comments_count: 3
repository_stars: 70862
---

When writing technical documentation, ensure it is accurate for real usage and immediately actionable for the reader (human or script). In practice:

- Flag exceptions explicitly (“caveats”): If behavior depends on provider/platform/version (e.g., hooks not running for some providers), include a clearly visible caveat section describing the affected cases and what the user should do.
- Don’t document misleading/implicit behavior: Avoid saying an option is “accepted but ignored.” If it’s not supported, remove it from reference tables and align docs with `--help`/actual behavior.
- For machine-readable output (`--json`, logs, events): specify the exact line structure and provide a schema-oriented description (what fields exist, and which record types a consumer should parse vs ignore). Include guidance like “skip types you don’t use.”

Example (output docs style):
```md
With `--json`, the CLI prints one JSON object per line. Every line includes `type` and `ts`.

Types:
- `run_result`: parse this for final text and usage
- `hook_event`: parse only if you consume hook lifecycle
- Other types: skip unless your script needs them
```