---
title: manage testing dependencies
description: Ensure testing dependencies are properly organized, avoid redundancy,
  and proactively manage unmaintained packages. Place testing-specific dependencies
  in the correct dependency groups (e.g., `group.test.dependencies` rather than `group.dev.dependencies`).
  Before adding new testing libraries, verify that existing dependencies don't already
  provide the same...
repository: python-poetry/poetry
label: Testing
language: Toml
comments_count: 3
repository_stars: 33496
---

Ensure testing dependencies are properly organized, avoid redundancy, and proactively manage unmaintained packages. Place testing-specific dependencies in the correct dependency groups (e.g., `group.test.dependencies` rather than `group.dev.dependencies`). Before adding new testing libraries, verify that existing dependencies don't already provide the same functionality - for example, use `pytest-mock` instead of adding a separate `mock` dependency. Monitor the maintenance status of testing dependencies and plan migration paths for stalled projects.

Example of proper dependency management:
```toml
[tool.poetry.group.test.dependencies]
pytest-httpserver = "^1.0.8"  # Correctly placed in test group
pytest-mock = ">=3.9"         # Use existing mock functionality
# Avoid: mock = "^2.0"         # Redundant with pytest-mock

# Plan migration for unmaintained dependencies
urllib3 = "<2.3"  # Temporary constraint due to httpretty compatibility
# TODO: Migrate from httpretty to mocket for better maintenance
```

This approach maintains a clean, maintainable test infrastructure while avoiding dependency conflicts and technical debt.