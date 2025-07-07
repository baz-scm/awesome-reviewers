---
title: Return collections not None
description: Return empty collections (lists, dicts, sets) instead of None when representing
  empty states. This reduces null checking boilerplate, prevents null reference errors,
  and makes code more predictable. When a function returns a collection type, an empty
  collection communicates "no items" more clearly than None and allows direct operations
  without defensive...
repository: open-telemetry/opentelemetry-python
label: Null Handling
language: Python
comments_count: 4
repository_stars: 2061
---

Return empty collections (lists, dicts, sets) instead of None when representing empty states. This reduces null checking boilerplate, prevents null reference errors, and makes code more predictable. When a function returns a collection type, an empty collection communicates "no items" more clearly than None and allows direct operations without defensive checks.

Example:
```python
# Not recommended
def extract_tags(span):
    if not span.tags:
        return None  # Forces callers to check for None
    return [tag for tag in span.tags]

# Recommended
def extract_tags(span):
    if not span.tags:
        return []  # Callers can immediately iterate/operate on result
    return [tag for tag in span.tags]

# Usage is simpler and safer
tags = extract_tags(span)
for tag in tags:  # Works directly, no None check needed
    process_tag(tag)
```

This pattern:
- Eliminates common None-check boilerplate
- Prevents NullPointerException scenarios
- Makes interfaces more predictable
- Allows direct operations on return values
- Maintains semantic clarity between "no items" vs "invalid/error state"

For error conditions or invalid states, raise exceptions or use Optional types instead of returning None.