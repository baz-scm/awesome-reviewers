---
title: Adapt for linter compatibility
description: When writing or modifying code, design patterns and templates to be compatible
  with linting tools. This is especially important for generated code and template
  systems.
repository: open-telemetry/opentelemetry-python
label: Code Style
language: Other
comments_count: 2
repository_stars: 2061
---

When writing or modifying code, design patterns and templates to be compatible with linting tools. This is especially important for generated code and template systems.

For templates that generate code, consider how linters will interpret the output:

```python
# Before - may trigger lint warnings when a variable has an inline comment
# VARIABLE: Final = 42
"""
Deprecated: This is being phased out.
"""

# After - linter-friendly approach
# VARIABLE: Final = 42
# Deprecated: This is being phased out.
```

For generated code (like protobuf files), prioritize proper lint fixes rather than disabling linters. When lint issues are complex, consider addressing them in dedicated PRs to maintain code quality without blocking other changes. Ensure that tooling configurations (like those in tox.ini) properly handle linting requirements for all code types in your project.