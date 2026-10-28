---
title: Verify documented behavior
description: Documentation must describe what the product actually does today, not
  what it used to do, is planned to do, or is assumed to do. Before publishing, verify
  every command, option, file path, and behavioral claim against the real implementation
  (run the command, grep the source, check logs with `lsof`, etc.) rather than trusting
  prior docs or assumptions —...
repository: cline/cline?x
label: Documentation
language: Other
comments_count: 8
repository_stars: 70983
---

Documentation must describe what the product actually does today, not what it used to do, is planned to do, or is assumed to do. Before publishing, verify every command, option, file path, and behavioral claim against the real implementation (run the command, grep the source, check logs with `lsof`, etc.) rather than trusting prior docs or assumptions — several inaccuracies here (wrong log paths, wrong option ordering in examples, an "enforces" claim that was really "supports") were only caught by tracing the actual code or running the command.

For features that are deprecated, broken, or silently no-ops (e.g., an env var that currently "has no effect", or a filter that no longer applies), don't leave them documented as if they work — that invites misuse and looks sloppy. Either:
- Remove the documentation entirely if the feature isn't coming back or isn't core to the product, or
- Keep it documented but add an explicit, visually distinct caveat (e.g., a `<Warning>` callout) stating it's currently broken/ignored and link the tracking issue, only when a fix is actively planned.

Avoid vague or non-exhaustive claims presented as complete (e.g., naming only two providers that run their own tool-calls when others do too) — either enumerate the full set or describe the general rule that lets a reader classify any case themselves. When wording implies a guarantee (e.g., "enforces"), confirm the mechanism actually guarantees it, and prefer weaker, accurate language ("supports", "applies") if it can be overridden.

Example of caveating a broken feature instead of silently documenting it as real:
```
| `CLINE_HOOKS_DIR` | Currently has no effect ([#14766](https://github.com/cline/cline/issues/14766)) |
```
instead of describing it as "Additional hooks directory" with no indication it's non-functional.