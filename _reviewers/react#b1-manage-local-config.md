---
title: Manage local config
description: Ensure configuration is cleanly separated between what’s shared and what’s
  environment/user-specific, and make any environment-specific install requirements
  explicit.
repository: facebook/react#b1
label: Configurations
language: Json
comments_count: 2
repository_stars: 251878
---

Ensure configuration is cleanly separated between what’s shared and what’s environment/user-specific, and make any environment-specific install requirements explicit.

Apply:
- User-specific local files (e.g., `settings.local.json`) must be gitignored; commit a shared `settings.json` (or equivalent) for common defaults.
- If changes introduce platform/toolchain-specific behavior or dependency workarounds (e.g., optional deps needing special install flags), document the required install command (e.g., in README) and keep dependencies in the appropriate scope (`devDependencies` vs `optionalDependencies`).

Example:
```gitignore
# user-specific overrides
compiler/.claude/settings.local.json
```
```json
// package.json
{
  "devDependencies": {
    "@playwright/test": "^1.41.2"
  },
  "optionalDependencies": {
    "fsevents": "1.2.13"
  }
}
```
And in documentation/README:
- Note the required install workaround, e.g., `yarn install --ignore-optional` (when applicable).