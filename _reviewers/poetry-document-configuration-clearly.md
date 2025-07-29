---
title: Document configuration clearly
description: Configuration files, hooks, and settings should include clear, accurate
  descriptions that explain their purpose and behavior. Descriptions should match
  the actual functionality and help developers understand what the configuration does
  and why it exists.
repository: python-poetry/poetry
label: Configurations
language: Yaml
comments_count: 4
repository_stars: 33496
---

Configuration files, hooks, and settings should include clear, accurate descriptions that explain their purpose and behavior. Descriptions should match the actual functionality and help developers understand what the configuration does and why it exists.

This prevents confusion when developers encounter unfamiliar configurations and reduces the cognitive load of understanding complex setups. Descriptions should be specific enough to distinguish between similar configurations and avoid misleading developers about the actual behavior.

Example of good configuration documentation:
```yaml
- id: poetry-lock-check
  name: poetry-lock-check
  description: check that poetry lock file is consistent with pyproject.toml
  
# Cron schedule with clear explanation
on:
  schedule:
    - cron: '0 * * * *'  # Run every hour at minute 0
```

Avoid vague descriptions that don't match the actual behavior, such as describing a hook as "synchronize dependencies" when it actually runs `poetry install --sync` by default, which may not be what users expect from a basic "install" operation.