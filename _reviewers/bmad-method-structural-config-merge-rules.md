---
title: Structural config merge rules
description: When adding or modifying skill/workflow customization, treat configuration
  resolution as a deterministic contract with (a) exact merge semantics and (b) clear
  config ownership/lifecycle.
repository: bmad-code-org/bmad-method
label: Configurations
language: Markdown
comments_count: 6
repository_stars: 51859
---

When adding or modifying skill/workflow customization, treat configuration resolution as a deterministic contract with (a) exact merge semantics and (b) clear config ownership/lifecycle.

## 1) Define the merge semantics precisely (and mirror them in any fallback)
Use these structural rules consistently for every customizable section (agents, workflows, and hooks):
- **Scalars:** later wins
- **Tables/objects:** deep-merge
- **Arrays that have `code` or `id` keys (menu-style):** merge by key
- **All other arrays:** append

If you provide a “manual merge fallback” when the resolver script fails, the fallback must restate and implement the **same** rules above—otherwise base sections like `principles`, `persistent_facts`, or `menu` can be silently dropped.

## 2) Respect config file ownership and regeneration
Treat installer-emitted files as **regenerated on every install** (read-only for durability):
- `_bmad/config.toml` and `_bmad/config.user.toml`

For durable overrides, commit only:
- `_bmad/custom/config.toml` (team)
- `_bmad/custom/config.user.toml` (personal)

## 3) Standardize config loading + variable resolution
Across SKILL.md/workflow.md, load from the standard config and resolve variables via the agreed path conventions (e.g., `{project-root}/_bmad/bmm/config.yaml`, and use placeholders like `{user_name}`, `{communication_language}`, `{planning_artifacts}` consistently). Avoid ad-hoc assumptions that diverge from the established pattern.

### Example (merge semantics contract)
When documenting or implementing fallback merge behavior, explicitly write:
```text
Merge rules:
- scalars: later wins
- tables: deep-merge
- arrays with {code,id}: merge by key
- other arrays: append
```