---
title: Document implementation contracts
description: 'Treat technical documentation—especially anything that developers will
  copy/paste or parse—as an implementation contract.


  Apply two rules:

  1) Make environment details explicit (especially filesystem paths)'
repository: cline/cline#v15
label: Documentation
language: Other
comments_count: 2
repository_stars: 70877
---

Treat technical documentation—especially anything that developers will copy/paste or parse—as an implementation contract.

Apply two rules:
1) Make environment details explicit (especially filesystem paths)
- Don’t assume `~` or shell expansion works the same for everyone.
- Provide OS-specific paths (e.g., Windows equivalents) or clearly define how a shorthand resolves (including profile/roaming nuances if relevant).

Example (plugins path docs):
- “Global: `~/.cline/plugins/` (macOS/Linux). Windows: `%USERPROFILE%\.cline\plugins\`. Project: `.cline/plugins/` (within the repo). Also supported: `~/Documents/Cline/Plugins/`.”

2) Make machine-readable formats precise (especially CLI/SDK JSON)
- Specify the exact wire format (e.g., “one JSON object per line” / JSONL).
- Document the schema at the level scripts need: required/meaningful fields, the `type` taxonomy, and what consumers must handle.
- Explicitly instruct readers to ignore event/status types they don’t need.
- Keep the reference aligned with current behavior; don’t list lines that no script should act on.

Example (JSON output docs):
- “With `--json`, output is JSON Lines: one JSON object per line. Every line includes `type` and `ts`.
  - Scripts should parse only the `type` values they care about and ignore the rest.”

Use these checks when updating any docs entry: “Can a Windows user resolve paths correctly without guessing?” and “Can a program writer reliably parse what to read and what to ignore?”