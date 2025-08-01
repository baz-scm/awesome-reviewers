---
title: Check before using values
description: Always validate that values are not null, undefined, or empty before
  using them in operations that depend on their content. This prevents downstream
  errors and unexpected behavior when collections are empty or strings are null.
repository: LMCache/LMCache
label: Null Handling
language: Python
comments_count: 2
repository_stars: 3800
---

Always validate that values are not null, undefined, or empty before using them in operations that depend on their content. This prevents downstream errors and unexpected behavior when collections are empty or strings are null.

When working with collections, check if they contain elements before proceeding with operations that assume non-empty data:

```python
# Before: Risk of empty collection causing issues downstream
for item in some_list:
    keys.append(item.key)
    memory_objs.append(item.memory_obj)
# subsequent logic assumes memory_objs is not empty

# After: Check collection before proceeding
if memory_objs:  # handles both None and empty cases
    # execute subsequent logic
```

For string values, use concise truthiness checks that handle both null and empty cases:

```python
# Before: Only checks for null
if chunk_message is not None:
    server_message.append(chunk_message)

# After: Handles both null and empty
if chunk_message:  # handles None, "", and other falsy values
    server_message.append(chunk_message)
```

This pattern prevents runtime errors and makes code more robust by ensuring operations only proceed when they have valid data to work with.