---
title: Document contracts and caveats
description: 'When writing or updating technical documentation (especially CLI/SDK
  behavior and machine-readable outputs), ensure the docs are:


  1) **Contract-accurate (no misleading options)**'
repository: cline/cline#v19
label: Documentation
language: Other
comments_count: 3
repository_stars: 70885
---

When writing or updating technical documentation (especially CLI/SDK behavior and machine-readable outputs), ensure the docs are:

1) **Contract-accurate (no misleading options)**
- If something is not actually supported or is not used, **omit it** from the reference tables or precisely document the real behavior.
- Avoid phrases like “accepted but ignored” unless the product truly guarantees that behavior.

2) **Exception-aware (add “caveats” where users can’t infer behavior)**
- For cases users can’t reasonably determine (e.g., which providers do internal tool processing vs. letting hooks run), add a small, practical **caveats** section explaining the affected class of cases.

3) **Parse-ready (define the exact I/O shape for automation)**
- For JSON outputs: specify **line format** (e.g., “one JSON object per line”), the required fields, and the meaning of `type` (and nested paths).
- Provide guidance for robust consumers: tell scripts to **skip types they don’t use** rather than forcing a complete exhaustive list.

Example pattern (JSON output parsing):
```md
With `--json`, the CLI prints one JSON object per line.
Each line includes `type` and `ts`.

- `type: agent_event` → payload is under `event`.
- `type: hook_event` → payload is under `event`.

Scripts should **ignore** `type` values they don’t need.
```

Apply this checklist to every docs change that affects runtime behavior, provider-specific differences, CLI flags, or any output intended for scripting.