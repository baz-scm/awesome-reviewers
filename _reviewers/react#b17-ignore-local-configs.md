---
title: Ignore local configs
description: Local/user-specific configuration should never be committed; commit only
  shared defaults/templates, and explicitly document any environment-specific install
  steps.
repository: facebook/react#b17
label: Configurations
language: Json
comments_count: 2
repository_stars: 251891
---

Local/user-specific configuration should never be committed; commit only shared defaults/templates, and explicitly document any environment-specific install steps.

Apply it by:
- Add user-specific files (e.g., `settings.local.json`) to `.gitignore`.
- Provide a committed, shareable config (e.g., `settings.json` or `settings.json.example`) and tell developers to create their local variant.
- If dependencies are platform/CI-specific (e.g., using `optionalDependencies`), document the exact install command required to avoid local platform issues.

Example:
```gitignore
# user-specific local overrides
compiler/.claude/settings.local.json
```
```json
// package.json (pattern)
{
  "devDependencies": { "@playwright/test": "^1.41.2" },
  "optionalDependencies": { "fsevents": "1.2.13" }
}
```
And in your README/CONTRIBUTING:
- “Install using `yarn install --ignore-optional` to ensure Linux compatibility.”