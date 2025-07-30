---
title: Centralize configuration sources
description: Maintain configuration settings in a single authoritative source to avoid
  duplication and inconsistencies across multiple files. When possible, use `pyproject.toml`
  as the primary configuration file and remove redundant specifications from other
  files like `.pre-commit-config.yaml` and `Makefile`.
repository: Unstructured-IO/unstructured
label: Configurations
language: Toml
comments_count: 2
repository_stars: 12117
---

Maintain configuration settings in a single authoritative source to avoid duplication and inconsistencies across multiple files. When possible, use `pyproject.toml` as the primary configuration file and remove redundant specifications from other files like `.pre-commit-config.yaml` and `Makefile`.

This approach follows the DRY (Don't Repeat Yourself) principle and ensures that configuration changes only need to be made in one place, reducing maintenance overhead and preventing configuration drift.

Example:
```toml
# pyproject.toml - Single source of truth
[tool.ruff.lint]
select = [
    "UP018",
    "UP032", 
    "UP034",
    "W",        # -- Warnings, including invalid escape-sequence --
]
ignore = [
    "COM812",
    "PT005",    # -- flags mock fixtures with names intentionally matching private method name --
    "PT011",
]
```

Remove redundant ruff configurations from `.pre-commit-config.yaml` and `Makefile` so they automatically pick up settings from `pyproject.toml`.