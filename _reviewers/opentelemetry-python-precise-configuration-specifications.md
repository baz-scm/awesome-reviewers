---
title: Precise configuration specifications
description: Ensure configuration files use tool-specific syntax and conventions while
  leveraging appropriate defaults. Be intentional about version constraints and conditionals
  in dependency specifications.
repository: open-telemetry/opentelemetry-python
label: Configurations
language: Toml
comments_count: 4
repository_stars: 2061
---

Ensure configuration files use tool-specific syntax and conventions while leveraging appropriate defaults. Be intentional about version constraints and conditionals in dependency specifications.

For tool configurations:
1. Use tool-specific syntax and options (e.g., for Pyright type ignores, use `pyright: ignore [error_code]` instead of `type: ignore [error_code]`)
2. Leverage built-in defaults when appropriate (e.g., Ruff automatically respects `.gitignore` files)
3. Be explicit about configuration modes (e.g., strict vs. standard type checking)

For dependency specifications:
1. Apply appropriate version constraints based on the package's versioning practices
2. Use platform/version conditionals for dependencies only required in specific environments
3. Be conservative with version ranges for packages that don't follow semantic versioning

Example:
```toml
# Good: Using tool-specific configuration with appropriate defaults
[tool.ruff]
target-version = "py38"
line-length = 79
# Not duplicating default excludes that already cover .tox, .venv, etc.

# Good: Using specific type ignore syntax
# In Python file: # pyright: ignore [specificError]
# For whole file: # pyright: strict, reportUnusedVariable=none

# Good: Proper dependency versioning with conditionals
dependencies = [
    "Deprecated >= 1.2.6",
    "importlib-metadata >= 6.0, <= 8.2.0; python_version < '3.10'",
]
```