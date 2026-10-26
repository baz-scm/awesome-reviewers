---
title: Accurate CLI Documentation
description: Documentation for commands and outputs should exactly match implementation
  behavior, be unambiguous for both humans and automation, and explicitly call out
  platform/path differences.
repository: cline/cline#v30
label: Documentation
language: Other
comments_count: 3
repository_stars: 70894
---

Documentation for commands and outputs should exactly match implementation behavior, be unambiguous for both humans and automation, and explicitly call out platform/path differences.

Apply this rule:
- Match reality: If a flag or field is removed or has a changed meaning, update docs accordingly; avoid documenting options as “accepted but ignored.”
- Align examples/tables with the CLI: examples should reflect what `--help` and actual execution do (including ordering/filters).
- Document only what consumers must handle: for machine-readable outputs (like JSONL), describe the line types/fields that matter to readers that parse them, and explicitly instruct scripts to ignore/skip types they don’t use.
- Clarify environment-dependent paths: if you use `~` or other shorthand, ensure it’s correct for all supported OSes (notably Windows) or document the exact additional locations (e.g., extra plugin directories) and how the path resolves for users.

Example (JSONL guidance pattern):
```md
With `--json`, the CLI prints one JSON object per line.
Scripts should only parse the event types they need; other line types may appear and can be skipped.
Each line includes `type` and `ts`.
```

Example (flag behavior clarity pattern):
- Do: update semantics in docs to match current behavior (e.g., ordering for `--limit`).
- Don’t: leave stale docs or mark behavior as “ignored” when users can’t rely on it.