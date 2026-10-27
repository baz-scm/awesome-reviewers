---
title: Document config and ignores
description: 'When configuration behavior is environment- or user-specific, keep overrides
  out of version control and make required build/install steps explicit.


  - Ignore user/local config files: add user-specific files (e.g., `settings.local.json`)
  to `.gitignore`. Provide a shared `settings.json` (or templates) for values that
  should be committed.'
repository: facebook/react#b14
label: Configurations
language: Json
comments_count: 2
repository_stars: 251893
---

When configuration behavior is environment- or user-specific, keep overrides out of version control and make required build/install steps explicit.

- Ignore user/local config files: add user-specific files (e.g., `settings.local.json`) to `.gitignore`. Provide a shared `settings.json` (or templates) for values that should be committed.
- If dependencies/config require environment-specific package-manager behavior (e.g., optionalDependencies, OS workarounds), document the exact install command/flags and the reason it’s needed so CI and dev machines stay reproducible.

Example:
```gitignore
# user-specific overrides
compiler/.claude/settings.local.json
```
```sh
# platform/package-manager workaround requiring optional deps to be ignored
yarn install --ignore-optional
```
```json
{
  "devDependencies": {
    "@playwright/test": "^1.41.2"
  },
  "optionalDependencies": {
    "fsevents": "1.2.13"
  }
}
```
