---
title: Reproducible configuration updates
description: 'When configuration changes depend on (a) filesystem paths or (b) dependency
  sources, make them both scope-complete and reproducible.


  1) Scope-complete path patterns (e.g., ignore files)'
repository: facebook/react#b12
label: Configurations
language: Other
comments_count: 2
repository_stars: 251896
---

When configuration changes depend on (a) filesystem paths or (b) dependency sources, make them both scope-complete and reproducible.

1) Scope-complete path patterns (e.g., ignore files)
- Don’t assume top-level patterns cover nested project directories.
- Example (adjust globs so they match nested locations too):
  ```gitignore
  # Ignore local Claude artifacts across the repo
  .claude/*.local.*
  compiler/.claude/*.local.*
  ```
  (If you currently use a top-level-only pattern like `/.claude`, extend it to cover nested `*/.claude` paths.)

2) Reproducible dependency/config sources (e.g., lockfiles)
- Treat lockfiles as configuration: if an install changes resolution, regenerate the relevant entries deliberately.
- Avoid unstable/custom install setups when they cause incompatible dependency hoisting; prefer stable local protocols such as `file:` or `link:` over ad-hoc `predev`-style sources.
  - Practical rule: if a dependency entry must change to restore compatibility, commit the updated lockfile and adjust the install source to a stable protocol so the issue doesn’t recur.

Use this checklist for any config-related PR: confirm path scope is correct; confirm dependency source/protocol stability; regenerate/commit lockfile changes intentionally when resolution changes.