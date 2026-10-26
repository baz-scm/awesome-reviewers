---
title: User-Centric Docs Accuracy
description: When updating technical documentation, ensure it is (1) accurate to real
  behavior, (2) proactive about caveats/edge cases, and (3) platform-complete—especially
  for Windows.
repository: cline/cline#v27
label: Documentation
language: Other
comments_count: 3
repository_stars: 70892
---

When updating technical documentation, ensure it is (1) accurate to real behavior, (2) proactive about caveats/edge cases, and (3) platform-complete—especially for Windows.

Apply this standard by:
- Add a visible “Caveats / Notes” section for non-obvious behavior or incomplete coverage. Don’t assume users know how integrations/providers work; explain the category of cases and what users can expect.
- Include platform-specific examples for paths and commands. If Unix-style paths or `~` are shown, also show the Windows equivalent (e.g., `%USERPROFILE%`-based paths) or clearly state how it resolves.
- Keep option/flag documentation strictly consistent with actual CLI/behavior. If an option is not actually used, don’t list it in a way that implies support—remove it or clearly mark the behavior in a way that matches truth (and validate against `--help`).
- Validate doc tables against source of truth (e.g., CLI `--help`, config output) so semantics like ordering/limits match.

Example (doc-table pattern that avoids misleading entries):

```md
## CLI Options

| Option | Description |
|--------|-------------|
| `--limit <count>` | Maximum number of sessions to show (newest first; default: 50) |

<!-- If a flag is accepted but ignored in practice, do not add it to this table. Remove it or adjust docs to match real behavior. -->
```

This standard reduces user confusion, prevents support churn caused by documentation drift, and makes cross-platform usage clearer.