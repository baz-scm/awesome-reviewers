---
title: Avoid shared structure mutation
description: When implementing algorithms that manipulate complex nested data structures,
  avoid directly mutating shared objects that might be referenced elsewhere in the
  system. Mutations can lead to unexpected side effects and hard-to-trace bugs, particularly
  when the same structure is referenced in multiple places.
repository: pydantic/pydantic
label: Algorithms
language: Python
comments_count: 2
repository_stars: 24364
---

When implementing algorithms that manipulate complex nested data structures, avoid directly mutating shared objects that might be referenced elsewhere in the system. Mutations can lead to unexpected side effects and hard-to-trace bugs, particularly when the same structure is referenced in multiple places.

Instead:
1. Create copies of data structures before modifying them
2. Use immutable data structures where possible
3. Consider the reference implications when extracting or moving properties between structures

For example, rather than:
```python
# Dangerous: directly mutating a schema that might be shared
schema = inner_schema['schema']
ref = schema.pop('ref', None)  # This modifies the original schema!
if ref:
    outer_schema['ref'] = ref
```

Prefer:
```python
# Safer: extract values without mutation
if 'ref' in inner_schema['schema']:
    ref = inner_schema['schema']['ref']
    outer_schema['ref'] = ref
    # Create a new structure without the ref if needed
    new_schema = {**inner_schema['schema']}
    new_schema.pop('ref')
```

This approach is especially important in schema generation, type systems, and other algorithms where complex nested structures with cross-references are common.