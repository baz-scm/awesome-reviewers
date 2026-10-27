---
title: Ignore Local Settings
description: Local or environment-specific configuration should not be blindly committed.
  Commit a shareable baseline config, ignore user-specific/local overrides, and explicitly
  document any environment- or tooling-specific install/config requirements (especially
  when optional dependencies or package-manager workarounds are involved).
repository: facebook/react#b4
label: Configurations
language: Json
comments_count: 2
repository_stars: 251885
---

Local or environment-specific configuration should not be blindly committed. Commit a shareable baseline config, ignore user-specific/local overrides, and explicitly document any environment- or tooling-specific install/config requirements (especially when optional dependencies or package-manager workarounds are involved).

Example:
```gitignore
# User-specific overrides
compiler/.claude/settings.local.json
```

Example (optional dependency/workaround + required install):
- If a workaround depends on skipping optional deps, make that requirement explicit in your repo docs or scripts, e.g.:
```sh
# For environments affected by the workaround
yarn install --ignore-optional
```
- Keep the “base” dependency/config in version control, and ensure developers understand the environment-specific installation steps needed to make it work reliably.