---
title: Safe attribute access pattern
description: Always use safe attribute access patterns to handle potentially null
  or undefined attributes. Instead of direct attribute access that might raise AttributeError,
  use `getattr()` with a default value. This pattern prevents null reference errors
  and makes code more robust.
repository: pydantic/pydantic
label: Null Handling
language: Python
comments_count: 4
repository_stars: 24377
---

Always use safe attribute access patterns to handle potentially null or undefined attributes. Instead of direct attribute access that might raise AttributeError, use `getattr()` with a default value. This pattern prevents null reference errors and makes code more robust.

Example:
```python
# Unsafe:
version = obj.__version__
value = obj.as_tuple()

# Safe:
version = getattr(obj, '__version__', '')
try:
    value = getattr(obj, 'as_tuple')()
except AttributeError:
    value = None
```

This approach:
1. Provides fallback values for missing attributes
2. Makes null cases explicit and handled
3. Reduces runtime errors from missing attributes
4. Makes code more maintainable by centralizing null handling

When using this pattern, choose meaningful default values that make sense in the context rather than always defaulting to None.