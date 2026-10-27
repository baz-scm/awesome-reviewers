---
title: Ignore local configs
description: 'Treat environment-specific configuration as non-uniform: keep user/local
  config files out of version control, and document any platform-specific dependency
  or install requirements.'
repository: facebook/react#b16
label: Configurations
language: Json
comments_count: 2
repository_stars: 251891
---

Treat environment-specific configuration as non-uniform: keep user/local config files out of version control, and document any platform-specific dependency or install requirements.

- Exclude user-specific files (e.g., `settings.local.json`) from git, and commit a shared base (e.g., `settings.json`) or example/template.
- If a dependency setup relies on OS-specific behavior or install flags (e.g., optional deps workaround), capture the exact command in docs/scripts (and/or CI) so contributors use the same setup.

Example:
```gitignore
# user-specific overrides
settings.local.json
# (optional) general pattern if applicable
*\.local\.json
```
```json
// settings.json (committed shared defaults)
{
  "someSetting": "default"
}
```
```sh
# documented install workaround when optional deps must be skipped
yarn install --ignore-optional
```