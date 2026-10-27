---
title: Local config hygiene
description: Do not commit user- or environment-specific configuration files. If a
  setting should be shared, commit a non-local config (e.g., `settings.json`) and
  keep local overrides untracked. If dependency setup includes OS-specific workarounds
  via `optionalDependencies`, document the required install command so all environments
  behave consistently.
repository: facebook/react#b10
label: Configurations
language: Json
comments_count: 2
repository_stars: 251894
---

Do not commit user- or environment-specific configuration files. If a setting should be shared, commit a non-local config (e.g., `settings.json`) and keep local overrides untracked. If dependency setup includes OS-specific workarounds via `optionalDependencies`, document the required install command so all environments behave consistently.

Example:
```gitignore
# User-specific/local overrides
compiler/.claude/settings.local.json
*settings.local.json
```

```json
// package.json (excerpt)
{
  "devDependencies": {
    "@playwright/test": "^1.41.2"
  },
  "optionalDependencies": {
    "fsevents": "1.2.13"
  }
}
```

```bash
# Document in README/CONTRIBUTING for consistent setup
yarn install --ignore-optional
```