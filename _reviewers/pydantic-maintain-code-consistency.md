---
title: Maintain code consistency
description: Ensure code follows consistent patterns throughout the codebase, even
  when duplicating code is necessary. When similar code patterns appear in multiple
  places, they should maintain the same structure and approach to improve readability
  and reduce errors.
repository: pydantic/pydantic
label: Code Style
language: Python
comments_count: 6
repository_stars: 24377
---

Ensure code follows consistent patterns throughout the codebase, even when duplicating code is necessary. When similar code patterns appear in multiple places, they should maintain the same structure and approach to improve readability and reduce errors.

Key practices:

1. **Use Pythonic idioms**: Prefer tuple unpacking in loops rather than index access.
   ```python
   # Instead of:
   for item in unsupported_attributes:
       attr, value = item[0], item[1]
       
   # Use:
   for attr, value in unsupported_attributes:
       # Code here
   ```

2. **Organize related code together**: Keep matching clauses and related logic together for better readability.
   ```python
   # Group similar conditionals together
   if isinstance(origin, TypeAliasType):
       return self._type_alias_type_schema(obj)
   # Other TypeAliasType related code...
   
   if _typing_extra.origin_is_union(origin):
       # Union related code
   ```

3. **Keep method signatures clean**: Remove unused parameters from method signatures.
   ```python
   # Instead of:
   def __init_subclass__(cls, **kwargs) -> None:
       # Method not using kwargs
       
   # Use:
   def __init_subclass__(cls) -> None:
       # Clean signature
   ```

4. **Maintain consistency across repetitions**: When similar code patterns must be repeated, ensure they follow the same approach.
   ```python
   # Use consistent patterns for similar operations
   model_frozen = cls.model_config.get('frozen')
   field_frozen = getattr(cls.__pydantic_fields__.get(name), 'frozen', False)
   if model_frozen or field_frozen:
       # First usage
   
   # Later in code:
   model_frozen = cls.model_config.get('frozen')
   # Same pattern as before
   ```

5. **Choose cleaner implementations**: When faced with multiple functionally equivalent options, choose the cleaner one.
   ```python
   # Instead of:
   field_info = FieldInfo._construct(metadata, **attr_overrides)
   if prepend_metadata is not None:
       field_info.metadata = prepend_metadata + field_info.metadata
   
   # Use:
   field_info = FieldInfo._construct(prepend_metadata + metadata, **attr_overrides)
   ```

Maintaining consistency reduces cognitive load when reading code, makes patterns more recognizable, and helps prevent subtle bugs from variations in similar code blocks.