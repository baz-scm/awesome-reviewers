---
title: explicit null checks
description: Use explicit null/undefined checks instead of methods that silently handle
  missing values. When you expect a value to be present, use access patterns that
  will fail fast if the value is missing rather than returning default values or silently
  continuing.
repository: bazelbuild/bazel
label: Null Handling
language: Other
comments_count: 3
repository_stars: 24489
---

Use explicit null/undefined checks instead of methods that silently handle missing values. When you expect a value to be present, use access patterns that will fail fast if the value is missing rather than returning default values or silently continuing.

**Prefer explicit checks that fail on missing values:**
- Use dictionary `[key]` instead of `get(key)` when the key must be present
- Use `!= None` instead of truthy checks when distinguishing null from empty collections
- Add bounds checking before accessing array/string elements

**Example from code review:**
```python
# Instead of using .get() which silently returns None:
ddi_file = source_to_ddi_file_map.get(source_artifact)

# Use direct access that fails if key is missing:
ddi_file = source_to_ddi_file_map[source_artifact]

# For collections, distinguish None from empty:
if lib.pic_objects != None:  # Not just: if lib.pic_objects:
    # Handle non-null collection (may be empty)
```

This approach makes your code more robust by catching bugs early when values are unexpectedly missing, rather than allowing silent failures that can be harder to debug later.