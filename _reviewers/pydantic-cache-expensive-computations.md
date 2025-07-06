---
title: Cache expensive computations
description: Implement strategic caching and memoization for expensive or frequently
  repeated computations to avoid redundant work. This can significantly improve performance
  in hot code paths.
repository: pydantic/pydantic
label: Performance Optimization
language: Python
comments_count: 5
repository_stars: 24377
---

Implement strategic caching and memoization for expensive or frequently repeated computations to avoid redundant work. This can significantly improve performance in hot code paths.

Key implementation strategies:

1. **Memoize frequently used functions or handlers** - Store the results of expensive lookups or computations that are repeatedly accessed with the same inputs
2. **Reuse complex structures** - When working with schemas, validators, or other complex objects, compute them once and reuse them where possible
3. **Implement proper cache invalidation** - Ensure caches are cleared or updated when the underlying data changes

Example of effective memoization:

```python
class BaseModel(metaclass=ModelMetaclass):
    __pydantic_setattr_handlers__: ClassVar[Dict[str, Callable[[BaseModel, Any], None]]]
    """__setattr__ handlers. Memoizing the setattr handlers leads to a dramatic 
    performance improvement in `__setattr__`"""
    
    def __setattr__(self, name: str, value: Any) -> None:
        # Use memoized handler for performance
        if (handler := self.__pydantic_setattr_handlers__.get(name)) is not None:
            handler(self, value)
            return
        # Fall back to slower path
```

For schema generation, reuse existing schemas rather than rebuilding them:

```python
# Previously: schema was generated twice for nested models
# Now: schema is only generated once and reused
schema = cls.__dict__.get('__pydantic_core_schema__')
if schema is not None and not isinstance(schema, MockCoreSchema):
    # Reuse the existing schema instead of rebuilding
    return schema
```

Remember to implement appropriate cache clearing when needed:

```python
# Clear cached values when they need to be rebuilt
for attr in ('__pydantic_core_schema__', '__pydantic_validator__', '__pydantic_serializer__'):
    if attr in cls.__dict__:
        delattr(cls, attr)
```