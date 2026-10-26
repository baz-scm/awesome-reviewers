---
title: Document Only What Works
description: 'Ensure documentation for CLI flags/config options reflects reality:
  never present “accepted but ignored” or no-effect options as working.


  Apply these rules:'
repository: cline/cline#v16
label: Documentation
language: Other
comments_count: 2
repository_stars: 70882
---

Ensure documentation for CLI flags/config options reflects reality: never present “accepted but ignored” or no-effect options as working.

Apply these rules:
- If an option/setting has no effect: remove the doc entry (and ideally the code path) or fix the product; avoid silent no-op documentation.
- If you must keep it temporarily: explicitly label it as broken/ignored with a clear caveat and an expected follow-up.
- Keep the docs synchronized with actual behavior and `--help`: verify defaults, result ordering, JSON shapes, and any semantics differences before landing reference updates.

Example pattern (from the discussions):
- Bad:
  - Docs says an option exists/works, but the release notes say it has no effect.
- Good:
  - Delete the row from the reference table, or change it to a clear caveat (broken/ignored) only when removal/fix is not viable.
- Also ensure semantics are correct, e.g. if `--limit` returns newest-first, the doc/table must say so.