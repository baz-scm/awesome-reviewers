---
title: Behavior-First Documentation
description: 'When updating docs, ensure they describe what users and scripts can
  reliably rely on.


  Apply these rules:

  1) Remove dead/no-op entries

  - Don’t keep options/fields in docs if they “have no effect” in the current release.'
repository: ClInE/cLiNe
label: Documentation
language: Other
comments_count: 3
repository_stars: 70838
---

When updating docs, ensure they describe what users and scripts can reliably rely on.

Apply these rules:
1) Remove dead/no-op entries
- Don’t keep options/fields in docs if they “have no effect” in the current release.
- Prefer deleting the row/section, or (only if you must keep it) clearly document the current behavior as a temporary exception with an explicit fix plan.

2) Keep docs aligned with real behavior
- Verify examples, defaults, option names, and ordering against the actual CLI/help text and implementation.
- If you discover a mismatch, fix the product OR update the docs by removing/adjusting the misleading statement (avoid “accepted but ignored” as a documentation strategy).

3) For structured/streamed outputs, document the parsing contract
- Don’t claim to enumerate every possible line/type.
- Specify stable fields and instruct consumers to skip/ignore types they don’t use.

Example (JSON output contract style)
```md
With `--json`, the CLI prints one JSON object per line.
Every line has a `type` and a `ts`.

Scripts should dispatch on `type` and ignore any types they don’t use.
Example event types include: ...
```