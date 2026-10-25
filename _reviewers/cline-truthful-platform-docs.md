---
title: Truthful, Platform Docs
description: 'Keep technical documentation strictly aligned with what the product/CLI
  actually does, and ensure examples work for the reader’s platform.


  Apply:

  - If a documented option/flag “has no effect,” do not keep it as “accepted but ignored.”
  Either (a) fix the product so it works, or (b) delete the documentation line/row
  until it works.'
repository: CLINE/cline
label: Documentation
language: Other
comments_count: 4
repository_stars: 70839
---

Keep technical documentation strictly aligned with what the product/CLI actually does, and ensure examples work for the reader’s platform.

Apply:
- If a documented option/flag “has no effect,” do not keep it as “accepted but ignored.” Either (a) fix the product so it works, or (b) delete the documentation line/row until it works.
- Treat authoritative sources (e.g., `--help`, actual command behavior, runtime output) as the ground truth. Update docs (tables, ordering, return semantics) when behavior changes.
- Document what readers/scripts must act on. Omit status/noise fields or event types that no consumer should parse.
- For path/location examples: don’t assume Unix semantics. Either provide Windows equivalents (e.g., `%USERPROFILE%/...`) or explicitly explain how `~` is resolved on Windows.

Example (doc accuracy pattern):
- Prefer removing a row for an ignored option rather than writing it as “ignored,” and ensure option descriptions match what users see:
  - ✅ Keep only options that work; verify against `cline --help` and real outputs.
  - ❌ Don’t document `CLINE_HOOKS_DIR` as functional when it “has no effect” in the release.