---
title: Defend against nulls
description: 'Always use defensive programming techniques when handling potentially
  null or empty values to avoid runtime errors. Consider these practices:


  1. Use specialized methods when checking for default values or null states rather
  than direct comparisons:'
repository: django/django
label: Null Handling
language: Python
comments_count: 4
repository_stars: 84182
---

Always use defensive programming techniques when handling potentially null or empty values to avoid runtime errors. Consider these practices:

1. Use specialized methods when checking for default values or null states rather than direct comparisons:
```python
# Prefer this
if self.has_default():
    # handle default case

# Instead of this
if self.default and self.default is not NOT_PROVIDED:
    # handle default case
```

2. Use `getattr()` with a default value when accessing attributes that might be None:
```python
# Safer approach
on_delete = getattr(field.remote_field, "on_delete", None)

# Instead of directly accessing which might raise AttributeError
# on_delete = field.remote_field.on_delete  # Risky if field.remote_field is None
```

3. Check if collections are non-empty before applying operations that could fail on empty sequences:
```python
# Safe handling of potentially empty collections
if objs and (order_wrt := self.model._meta.order_with_respect_to):
    # process objects

# Instead of assuming collection is non-empty
```

4. Be aware of different types of nulls in specialized contexts (e.g., SQL NULL vs JSON null):
```python
# SQL NULL
obj.json_field = None
# JSON null (different semantics in queries)
obj.json_field = Value(None, output_field=JSONField())
```

These defensive patterns prevent common null-related errors and make code more robust.