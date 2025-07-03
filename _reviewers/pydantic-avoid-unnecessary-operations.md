---
title: Avoid unnecessary operations
description: Check conditions early to skip unnecessary processing and reuse computed
  values where possible to optimize performance. This reduces CPU cycles and improves
  execution speed, especially in performance-critical code paths.
repository: pydantic/pydantic
label: Performance Optimization
language: Python
comments_count: 2
repository_stars: 24364
---

Check conditions early to skip unnecessary processing and reuse computed values where possible to optimize performance. This reduces CPU cycles and improves execution speed, especially in performance-critical code paths.

**Early condition checking example:**
```python
# Less performant approach
def process_value(assigned_value):
    # Perform expensive operations regardless of value state
    result = complex_calculation(assigned_value)
    if assigned_value is PydanticUndefined:
        return default_value
    return result

# More performant approach
def process_value(assigned_value):
    # Early check avoids unnecessary processing
    if assigned_value is PydanticUndefined:
        return default_value
    result = complex_calculation(assigned_value)
    return result
```

**Value caching example:**
```python
def get_schema(cls: type) -> Schema:
    # Check if schema already exists before regenerating
    schema = cls.__dict__.get('__schema__')
    if (
        schema is not None
        and not isinstance(schema, MockSchema)
        and conditions_for_reuse_met(cls)
    ):
        return schema
    
    # Only build new schema when necessary
    return build_new_schema(cls)
```

Apply these patterns whenever you find yourself performing expensive operations that might be unnecessary based on input conditions or when values can be safely reused across calls.