---
title: Explicit null handling
description: Always be explicit and consistent about how null values are handled in
  operations and documentation. This clarity prevents confusion and ensures predictable
  behavior across the codebase.
repository: pola-rs/polars
label: Null Handling
language: Python
comments_count: 6
repository_stars: 34296
---

Always be explicit and consistent about how null values are handled in operations and documentation. This clarity prevents confusion and ensures predictable behavior across the codebase.

When implementing functions that process data which might contain nulls:

1. Use "null" terminology (not "None") in documentation and comments to maintain conceptual consistency, even though Python uses `None` internally:
```python
# Incorrect
def eq_missing(self, other: Any) -> Self:
    """Equality operator where `None` is treated as a distinct value."""

# Correct
def eq_missing(self, other: Any) -> Self:
    """Equality operator where null is treated as a distinct value."""
```

2. Document null behavior with concrete examples:
```python
def sum_horizontal(*columns, ignore_nulls: bool = True):
    """Sum values horizontally across columns.
    
    Parameters
    ----------
    ignore_nulls
        - If True: nulls are replaced by 0 (e.g., 1 + null + 2 = 3)
        - If False: nulls are propagated (e.g., 1 + null + 2 = null)
    """
```

3. When documenting behavior, avoid double negations and use clear, specific language:
```python
# Avoid: "If there are no non-null values, the output is False."
# Better: "If all values are null or the collection is empty, the output is False."
```

4. For operations where input values might not match expected size/format, explicitly state how nulls are used:
```python
# Example: Document how binary data of incorrect length is handled
"""Note that rows of the binary array where the length does not match 
the width of the output array will become NULL."""
```

Consistently following these practices reduces ambiguity and helps users understand how their data will be processed in the presence of missing values.