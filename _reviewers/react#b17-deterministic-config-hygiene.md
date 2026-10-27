---
title: Deterministic Config Hygiene
description: 'Keep configuration (paths and dependency install/protocol setup) deterministic
  and correctly scoped so dev environments don’t diverge.


  Apply this:

  1) Scope configuration patterns to all relevant directories'
repository: facebook/react#b17
label: Configurations
language: Other
comments_count: 2
repository_stars: 251891
---

Keep configuration (paths and dependency install/protocol setup) deterministic and correctly scoped so dev environments don’t diverge.

Apply this:
1) Scope configuration patterns to all relevant directories
- When ignoring generated/tool artifacts, confirm the glob covers nested locations (not just the top-level). For example, if you need to ignore Claude local files, prefer patterns that include subdirectories like:
```gitignore
# Tool-generated Claude local state (top-level + nested)
.claude/*.local.*
compiler/.claude/*.local.*
```
(Using `/.claude/...` would miss nested `./compiler/.claude/...`-style paths.)

2) Make dependency installation deterministic
- Avoid install setups that change package resolution/hoisting in unexpected ways (e.g., “predev” leading to an older transitive setup and incompatible hoisting). Prefer stable local dependency protocols such as `file:` or `link:` so Yarn computes a consistent dependency graph.
- After changing install/protocol/config inputs, regenerate and commit the lockfile so the repo matches what developers actually install.

Result: fewer environment-specific surprises, fewer broken builds due to mismatched ignored artifacts or incompatible dependency hoisting.