---
title: Eliminate redundant computation
description: Identify and eliminate redundant or duplicate computation paths in your
  code, especially for expensive operations like schema generation, type resolution,
  or recursive traversals. This improves performance and reduces resource usage.
repository: pydantic/pydantic
label: Algorithms
language: Python
comments_count: 5
repository_stars: 24377
---

Identify and eliminate redundant or duplicate computation paths in your code, especially for expensive operations like schema generation, type resolution, or recursive traversals. This improves performance and reduces resource usage.

Key practices to follow:
1. Cache expensive computation results when they won't change between calls
2. Analyze code paths to identify duplicate work
3. Use appropriate method ordering to avoid repeated expensive operations
4. Consider specialized implementations for frequently used operations

Example of problematic code:
```python
def _display_complex_type(obj: Any) -> str:
    # Expensive recursive operation called frequently
    if get_origin(obj):
        args = get_args(obj)
        # Recursive processing of each argument...
    # ...

# Called in multiple places
repr_args = _display_complex_type(type_)  # Called repeatedly for same types
```

Improved approach:
```python
@cached_property  # Or use functools.lru_cache
def _validator(self) -> SchemaValidator:
    """Cache validator to avoid rebuilding for each validation"""
    if not self._core_schema:
        self._build_schema()  # Build only once
    return SchemaValidator(self._core_schema)
```

For frequently used utility functions, consider specialized implementations that avoid repeated work or use more efficient algorithms for common cases.