---
title: Shared vs Local Config
description: Keep configuration split into (1) repo-shared defaults and (2) user/environment-specific
  overrides, and make any required environment setup steps explicit.
repository: facebook/react#b9
label: Configurations
language: Json
comments_count: 2
repository_stars: 251891
---

Keep configuration split into (1) repo-shared defaults and (2) user/environment-specific overrides, and make any required environment setup steps explicit.

- **Do not commit user-local files** (e.g., `settings.local.json`). Add them to **`.gitignore`**.
- **Provide a shared base** (e.g., `settings.json` or a template) that developers can copy/override locally.
- **When a config change depends on an environment workaround**, document it in setup instructions and ensure the correct install command/flags are used for that environment.

Example (setup + config split):
```json
// .gitignore
compiler/.claude/settings.local.json
```
```bash
# README / setup script: document required flags for environment-specific installs
# e.g., Linux workaround requiring optional deps to be ignored
yarn install --ignore-optional
```
```json
// shared settings committed to repo
// compiler/.claude/settings.json
{
  "someSharedSetting": true
}
```
Developers then create a local override (untracked) such as `settings.local.json` based on the shared template.