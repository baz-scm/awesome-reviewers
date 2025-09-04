---
title: API backward compatibility
description: Maintain backward compatibility when evolving API interfaces by preserving
  existing method signatures and parameter patterns. When adding new functionality,
  prefer extending existing interfaces over breaking changes, and use deprecation
  warnings for obsolete parameters.
repository: stanfordnlp/dspy
label: API
language: Python
comments_count: 6
repository_stars: 27813
---

Maintain backward compatibility when evolving API interfaces by preserving existing method signatures and parameter patterns. When adding new functionality, prefer extending existing interfaces over breaking changes, and use deprecation warnings for obsolete parameters.

Key principles:
1. **Preserve existing signatures**: Avoid changing method signatures that users depend on, as noted: "This signature cannot be changed, we do need to handle the case where users directly call `get`"
2. **Use kwargs for flexibility**: Support both initialization-time and call-time parameters: "It's important that users can set kwargs in `__init__`, which become defaults for `__call__`. The `kwargs` passed to `__call__` overwrite any defaults from `__init__`"
3. **Deprecate gracefully**: Instead of removing parameters immediately, use deprecation warnings and **kwargs to maintain compatibility: "We can introduce the wildcard `kwargs` and move the deprecated args there, and print a clear warning that it's deprecated"
4. **Design for evolution**: Structure APIs to accept configuration through method parameters rather than constructor-only initialization, enabling reuse across different contexts

Example of backward-compatible parameter evolution:
```python
# Before
def __init__(self, model):
    self.model = model

# After - maintains compatibility while adding type safety
def __init__(self, embedding_model: Union[str, Callable] = 'text-embedding-ada-002', 
             embedding_function: Optional[Callable] = None, **kwargs):
    # Handle both old and new parameter patterns
    self.model = embedding_function or embedding_model
    self.kwargs = kwargs
```

This approach prevents breaking existing user code while enabling clean API evolution and improved developer experience.