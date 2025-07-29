---
title: API backwards compatibility
description: When evolving public APIs, prioritize backwards compatibility through
  proper deprecation strategies and careful interface design. Avoid breaking changes
  by using overloads, deprecation warnings, and gradual migration paths.
repository: python-poetry/poetry
label: API
language: Python
comments_count: 4
repository_stars: 33496
---

When evolving public APIs, prioritize backwards compatibility through proper deprecation strategies and careful interface design. Avoid breaking changes by using overloads, deprecation warnings, and gradual migration paths.

Key principles:
- Use method overloads to maintain existing signatures while adding new functionality
- Keep implementation details private to avoid coupling external code to internal changes  
- Deprecate old parameters/methods before removing them, providing clear migration paths
- Consider the impact on plugins and external consumers when making API changes

Example approach for adding new parameters:
```python
def add_repository(
    self,
    repository: Repository,
    priority: Priority = Priority.PRIMARY,
    # Keep old parameters for backwards compatibility
    default: bool = False, 
    secondary: bool = False
) -> None:
    # Handle both old and new parameter styles
    if default or secondary:
        warnings.warn("default/secondary parameters are deprecated, use priority instead")
```

This ensures external code continues working while providing a clear upgrade path. Always weigh the benefits of cleaner APIs against the cost of breaking existing integrations.