---
title: Manage local configs
description: 'Treat configuration as environment-specific: commit only shareable configuration,
  and clearly document any setup/install flags required by OS or platform workarounds.'
repository: facebook/react#b15
label: Configurations
language: Json
comments_count: 2
repository_stars: 251891
---

Treat configuration as environment-specific: commit only shareable configuration, and clearly document any setup/install flags required by OS or platform workarounds.

- Ignore user-specific local config files (e.g., `settings.local.json`) and keep a separate shared file (e.g., `settings.json`) for common settings.
- If dependency or config changes rely on platform quirks or optional dependencies, capture the required install command/flags in the repo docs (e.g., use `--ignore-optional` when noted).

Example:

```gitignore
# User/machine-specific
compiler/.claude/settings.local.json
```

```bash
# Document when optional deps must be skipped due to platform/workaround
yarn install --ignore-optional
```