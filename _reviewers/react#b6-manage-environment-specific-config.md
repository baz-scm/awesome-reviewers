---
title: Manage environment-specific config
description: When configuration or dependencies differ by environment or user, keep
  the variability out of committed shared state and make the remaining setup reproducible.
repository: facebook/react#b6
label: Configurations
language: Json
comments_count: 2
repository_stars: 251888
---

When configuration or dependencies differ by environment or user, keep the variability out of committed shared state and make the remaining setup reproducible.

Apply this by:
- **Gitignore user/local config files** (e.g., `settings.local.json`) and provide a **tracked shared default** (e.g., `settings.json`).
- **Treat platform workarounds as documented setup steps**: if a dependency requires a workaround on specific OSes, make that workaround explicit (e.g., via documented install flags or a repo script) and keep the workaround-dependent pieces optional.

Example (recommended patterns):
```bash
# Example setup script (documented requirement)
yarn install --ignore-optional
```
```gitignore
# User-specific settings should not be committed
compiler/.claude/settings.local.json
```
```json
// Shared config should be committed (example placeholder)
// compiler/.claude/settings.json
{ }
```
This ensures developers have a consistent baseline while still supporting environment-specific behavior safely.