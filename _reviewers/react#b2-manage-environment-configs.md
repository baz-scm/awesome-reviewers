---
title: Manage environment configs
description: 'Ensure configuration is handled explicitly for different environments
  and machines.


  - Don’t commit user/machine-specific files (e.g., `settings.local.json`). Add them
  to `.gitignore`; keep only shareable defaults like `settings.json`.'
repository: facebook/react#b2
label: Configurations
language: Json
comments_count: 2
repository_stars: 251882
---

Ensure configuration is handled explicitly for different environments and machines.

- Don’t commit user/machine-specific files (e.g., `settings.local.json`). Add them to `.gitignore`; keep only shareable defaults like `settings.json`.
- When environment-specific dependency behavior is required (OS/package-manager quirks), declare the dependencies appropriately (e.g., dev vs optional) and document/enforce the required install steps (e.g., using install flags such as `--ignore-optional`).

Example (typical patterns):
```gitignore
# user-specific local config
compiler/.claude/settings.local.json
```
```json
// package.json snippet
{
  "devDependencies": {
    "@playwright/test": "^1.41.2"
  },
  "optionalDependencies": {
    "fsevents": "1.2.13"
  }
}
```
```sh
# install step required by environment/dependency workaround
yarn install --ignore-optional
```