---
title: synchronize configuration environments
description: Ensure configuration values remain consistent between local development
  and CI/CD environments, and document the rationale behind environment-specific settings.
  Version mismatches and undocumented configuration behavior can lead to unexpected
  failures and developer confusion.
repository: stanfordnlp/dspy
label: Configurations
language: Yaml
comments_count: 2
repository_stars: 27813
---

Ensure configuration values remain consistent between local development and CI/CD environments, and document the rationale behind environment-specific settings. Version mismatches and undocumented configuration behavior can lead to unexpected failures and developer confusion.

When updating configuration values like dependency versions, tool versions, or environment variables, verify they match across all environments. Add explanatory comments for configurations that have non-obvious behavior or requirements.

Example:
```yaml
env:
  # Keep in sync with poetry.lock - developers use 1.7.1 locally
  POETRY_VERSION: "1.7.1"

- name: Create test environment
  # Virtual env activation changes sys.path, excluding working dir
  # Installation is required for imports to work properly
  run: python -m venv test_env
```

Regularly audit configuration files to catch drift between local development tools and CI/CD pipeline settings.