---
title: Verify configuration options
description: Always verify that configuration file options and command flags are correct
  and properly documented. Incorrect configuration syntax can cause silent failures
  or unintended side effects that are difficult to debug.
repository: python-poetry/poetry
label: Configurations
language: Other
comments_count: 2
repository_stars: 33496
---

Always verify that configuration file options and command flags are correct and properly documented. Incorrect configuration syntax can cause silent failures or unintended side effects that are difficult to debug.

Common issues include:
- Using deprecated or non-existent configuration options that fail silently
- Using commands without appropriate flags that cause broader changes than intended

Before committing configuration changes:
1. Check official documentation for correct option names and syntax
2. Use specific flags to limit scope of operations (e.g., `poetry lock --no-update` instead of `poetry lock`)
3. Test configuration changes to ensure they work as expected

Example from the discussions:
```
# Wrong - silently breaks functionality
[flake8]
enable-select = TC, TC1

# Correct - properly documented option
[flake8] 
extend-select = TC, TC1
```

```bash
# Wrong - updates all dependencies unintentionally
poetry lock

# Correct - only regenerates lock without updating versions
poetry lock --no-update
```