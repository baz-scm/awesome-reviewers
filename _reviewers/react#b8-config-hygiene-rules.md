---
title: Config hygiene rules
description: 'Treat config/tool-generated files and install configuration as first-class,
  deterministic inputs:


  - Scope `.gitignore`/config artifact rules across the whole repo: local or generated
  tool directories must be ignored everywhere they may appear (not only at the top
  level). For example, if you add `+.claude/*.local.*`, also ensure equivalent nested
  paths are...'
repository: facebook/react#b8
label: Configurations
language: Other
comments_count: 2
repository_stars: 251889
---

Treat config/tool-generated files and install configuration as first-class, deterministic inputs:

- Scope `.gitignore`/config artifact rules across the whole repo: local or generated tool directories must be ignored everywhere they may appear (not only at the top level). For example, if you add `+.claude/*.local.*`, also ensure equivalent nested paths are covered (e.g., under `compiler/`).
- Prefer stable dependency/install configuration: avoid install protocols that lead to incompatible hoisting or mismatched dependency graphs (e.g., replacing `predev` with `file:` or `link:` where appropriate). When the resolved dependency graph changes, regenerate and commit the relevant `yarn.lock` entries by re-running install (rather than editing lock entries by hand).

Example adjustments:
```gitignore
# Ignore local tool-generated files at all relevant locations
.claude/*.local.*
compiler/.claude/*.local.*
```
```text
# Prefer stable protocols
# instead of predev, use file: or link: so resolution/hoisting stays compatible
```