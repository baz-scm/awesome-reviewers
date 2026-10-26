---
title: Accurate, Consumable Docs
description: When updating technical documentation, ensure it (1) matches the actual
  product behavior, (2) is safe/clear for the target platforms and users, and (3)
  provides a real parsing/usage contract for consumers (scripts, CLI users), not just
  a list.
repository: cline/cline#v28
label: Documentation
language: Other
comments_count: 3
repository_stars: 70893
---

When updating technical documentation, ensure it (1) matches the actual product behavior, (2) is safe/clear for the target platforms and users, and (3) provides a real parsing/usage contract for consumers (scripts, CLI users), not just a list.

Apply these rules:
- Platform correctness: For filesystem paths, don’t rely on ambiguous shell shortcuts alone. If you document a location using `~`, also provide an equivalent Windows form (or an explicit Windows path) so Windows users aren’t guessing.
- Behavioral fidelity: Every CLI option and description must reflect what the command truly does. Remove or rewrite entries for options that were removed/ignored; avoid implying “accepted but ignored” behavior.
- Contract-first output formats: For structured outputs (e.g., JSONL), document the stable fields and the set of meaningful record types, and instruct readers what to do with record types they don’t care about (e.g., skip unknown/unneeded types). Don’t clutter tables with status lines that no consumer should act on.

Example (JSONL consumer guidance):
```md
With `--json`, the CLI prints one JSON object per line. Each line has `type` and `ts`.

For scripts: handle only the record types you use; skip the rest.
Example types include: `agent_event`, `hook_event`, `run_result`, `run_aborted`.
```

Example (cross-platform paths):
```md
Global plugins are loaded from:
- macOS/Linux: `~/.cline/plugins/`
- Windows: `%USERPROFILE%\.cline\plugins\`

Cline also loads from the Documents plugin folder:
- macOS/Linux: `~/Documents/Cline/Plugins/`
- Windows: `%USERPROFILE%\Documents\Cline\Plugins\`
```