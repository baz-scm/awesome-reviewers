---
title: validate before data access
description: Always validate for null or None values before accessing data elements,
  especially when working with collections or optional parameters. Avoid direct indexing
  or attribute access without first ensuring the data exists and is valid.
repository: apache/spark
label: Null Handling
language: Python
comments_count: 2
repository_stars: 41554
---

Always validate for null or None values before accessing data elements, especially when working with collections or optional parameters. Avoid direct indexing or attribute access without first ensuring the data exists and is valid.

When accessing elements from collections that may contain nulls, filter out null values first rather than assuming the first element is valid:

```python
# Instead of direct access:
# return pser.iloc[0].__UDT__

# Filter nulls first, then access:
notnull = pser[pser.notnull()]
if len(notnull) > 0 and hasattr(notnull.iloc[0], "__UDT__"):
    return notnull.iloc[0].__UDT__
```

Additionally, maintain consistent patterns for handling None vs empty collections in function parameters to avoid confusion and potential bugs. If a function expects a list but receives None, establish a clear convention (either convert None to empty list, or handle None explicitly) and apply it consistently across the codebase.