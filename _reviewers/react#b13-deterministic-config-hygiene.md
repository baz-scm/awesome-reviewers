---
title: Deterministic Config Hygiene
description: 'Keep configuration changes reproducible and correctly scoped—both for
  local/generated artifacts and for dependency resolution.


  Apply this when updating `.gitignore`, fixture setups, or dependency installation
  scripts:'
repository: facebook/react#b13
label: Configurations
language: Other
comments_count: 2
repository_stars: 251893
---

Keep configuration changes reproducible and correctly scoped—both for local/generated artifacts and for dependency resolution.

Apply this when updating `.gitignore`, fixture setups, or dependency installation scripts:
- **Scope ignore patterns to the real paths**: ensure patterns cover nested directories (e.g., top-level patterns like `/.claude` won’t match `./compiler/.claude`).
- **Use deterministic dependency linkage**: avoid custom/nonstandard install mechanisms that can trigger incompatible hoisting and lockfile churn (e.g., replace `predev` with stable `file:` or `link:` protocols). After changing linkage, **regenerate** affected `yarn.lock` entries.

Example `.gitignore` adjustment pattern:
```gitignore
# Ignore Claude local artifacts everywhere (including nested tool directories)
/.claude/*.local.*
/compiler/.claude/*.local.*
```

Example dependency linkage guidance (conceptual):
- Prefer `file:` or `link:` to source packages/fixtures rather than `predev`, then run `yarn install` and commit the resulting `yarn.lock` updates so fixture installs remain consistent.