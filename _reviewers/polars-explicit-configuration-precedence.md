---
title: Explicit configuration precedence
description: 'Implement a clear configuration resolution chain that follows a consistent
  precedence pattern: explicit parameters first, then environment variables, then
  default values. This ensures predictable behavior and proper respect for user-provided
  settings at different levels.'
repository: pola-rs/polars
label: Configurations
language: Python
comments_count: 5
repository_stars: 34296
---

Implement a clear configuration resolution chain that follows a consistent precedence pattern: explicit parameters first, then environment variables, then default values. This ensures predictable behavior and proper respect for user-provided settings at different levels.

When a parameter can be configured through multiple means (function parameters, environment variables, config files), default it to `None` in function signatures and explicitly handle the resolution sequence in your code:

```python
def process_data(engine=None):
    # Check explicit parameter first
    if engine is None:
        # Then check environment variable
        engine = get_engine_from_environment()
        if engine is None:
            # Finally use the default value
            engine = "cpu"
```

This approach offers several benefits:
- Users can understand and predict which configuration source takes precedence
- Function calls without explicit parameters will respect environment configurations
- You can track the source of a configuration setting for better error messages
- The code clearly documents the fallback behavior
- It becomes easier to add new configuration sources without breaking existing code

When documenting these parameters, clearly communicate the precedence chain so users understand how their configurations will be applied.