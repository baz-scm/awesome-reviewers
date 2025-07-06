---
title: Hide implementation details
description: Design public APIs to hide implementation details and focus on the user's
  mental model of the system. Avoid exposing internal classes, implementation-specific
  parameters, or technical approaches that might change in the future.
repository: pola-rs/polars
label: API
language: Python
comments_count: 5
repository_stars: 34296
---

Design public APIs to hide implementation details and focus on the user's mental model of the system. Avoid exposing internal classes, implementation-specific parameters, or technical approaches that might change in the future.

Key principles:
- Use terminology that matches the user's conceptual model, not internal implementation
- Avoid exposing implementation-specific parameters like `parallel` or internal classes
- Prefer extensible parameter designs (e.g., string literals) over booleans for features that might be expanded
- Use full descriptive names in public APIs instead of abbreviations

Example - Before:
```python
def set_gpu_engine(cls, active: bool | None = None) -> type[Config]:
    """Set the default engine to use the GPU."""
    # ...

def filter(self, predicate: Expr, *, parallel: bool = False) -> Series:
    """Filter elements in each list by a boolean expression."""
    # ...
```

Example - After:
```python
def set_default_engine(cls, engine: Literal["cpu", "gpu"]) -> type[Config]:
    """Set the default engine type."""
    # ...

def filter(self, predicate: Expr) -> Series:
    """Filter elements in each list by a boolean expression."""
    # ...
```

This approach creates more maintainable APIs, gives implementation flexibility, and provides a clearer mental model for users.