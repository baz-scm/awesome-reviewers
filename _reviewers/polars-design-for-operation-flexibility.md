---
title: Design for operation flexibility
description: 'When implementing algorithms that operate on data structures (particularly
  arrays, lists, or collections), design them to handle both constant and expression-based
  inputs efficiently. Consider the constraints each imposes on the algorithm:'
repository: pola-rs/polars
label: Algorithms
language: Python
comments_count: 4
repository_stars: 34296
---

When implementing algorithms that operate on data structures (particularly arrays, lists, or collections), design them to handle both constant and expression-based inputs efficiently. Consider the constraints each imposes on the algorithm:

1. For constant inputs, you can determine output shapes/types at compile-time
2. For expression-based inputs, you may need runtime evaluation

Implement pattern flags (like `as_array`) that indicate when constant values are required for type determination. This enables both flexibility and performance optimization.

For example:
```python
def slice(self, offset: int | Expr, length: int | Expr, as_array: bool = True) -> Expr:
    """Slice the array.
    
    Parameters
    ----------
    offset
        The offset to start the slice.
    length
        The length of the slice.
    as_array
        If True, offset and length must be constants.
        If False, returns a list instead of an array.
    """
    if as_array and (not isinstance(offset, int) or not isinstance(length, int)):
        raise ValueError("When as_array=True, offset and length must be constants")
    
    # Implementation continues...
```

This pattern enables algorithms to work efficiently with both scenarios while providing clear feedback when constraints cannot be met.