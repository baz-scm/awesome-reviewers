---
title: Local config hygiene
description: 'Ensure configuration is reproducible and not user-specific:


  - Don’t commit user/local config files (e.g., anything named `*.local.*`): add them
  to `.gitignore` and keep any shared defaults in a non-local file (e.g., `settings.json`)
  or a checked-in template.'
repository: facebook/react#b3
label: Configurations
language: Json
comments_count: 2
repository_stars: 251883
---

Ensure configuration is reproducible and not user-specific:

- Don’t commit user/local config files (e.g., anything named `*.local.*`): add them to `.gitignore` and keep any shared defaults in a non-local file (e.g., `settings.json`) or a checked-in template.
- If the configuration depends on platform-specific workarounds or optional dependency behavior, document the exact setup/install command (including required flags) so new devs and CI run it the same way.

Example:
- `.gitignore`
  - `compiler/.claude/settings.local.json`
- `README`/setup notes
  - “On Linux, run: `yarn install --ignore-optional` (workaround requires optional deps to be ignored).”