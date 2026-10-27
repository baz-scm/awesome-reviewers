---
title: Manage Config Hygiene
description: Ensure configuration artifacts are clearly separated by scope (shared
  vs user/environment-specific) and that any environment-dependent install/workaround
  requirements are documented and reproducible.
repository: facebook/react#b5
label: Configurations
language: Json
comments_count: 2
repository_stars: 251886
---

Ensure configuration artifacts are clearly separated by scope (shared vs user/environment-specific) and that any environment-dependent install/workaround requirements are documented and reproducible.

- **Do not commit user- or machine-specific files** (e.g., `settings.local.json`). Add them to `.gitignore` and provide a shareable `settings.json` (or equivalent) for common configuration.
- **If configuration requires special install behavior**, make it explicit and repeatable (e.g., required flags like `--ignore-optional`). Prefer encoding these steps in package scripts or setup docs so team members don’t hit inconsistent environments.

Example pattern:
```json
// .gitignore
compiler/.claude/settings.local.json
```
```json
// package.json (example script to make the workaround repeatable)
{
  "scripts": {
    "setup": "yarn install --ignore-optional"
  }
}
```