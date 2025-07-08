---
title: Structure for readability
description: Structure code to maximize readability by reducing unnecessary complexity.
  Use early returns to minimize nesting levels, move invariant conditions outside
  of loops, and replace magic numbers with named constants.
repository: pytorch/pytorch
label: Code Style
language: Python
comments_count: 3
repository_stars: 91345
---

Structure code to maximize readability by reducing unnecessary complexity. Use early returns to minimize nesting levels, move invariant conditions outside of loops, and replace magic numbers with named constants.

Example - Replace deeply nested conditions:
```python
# Instead of this:
def estimate_flops(self) -> int | None:
    if isinstance(self, ExternKernel):
        if op is not None:
            # Deep logic here
            pass
    return None

# Prefer this:
def estimate_flops(self) -> int | None:
    if not isinstance(self, ExternKernel) or op is None:
        return None
    # Logic continues at a single nesting level
```

Similarly, when a condition inside a loop doesn't change between iterations, move it outside:
```python
# Instead of checking the same condition in each iteration
for i, future in enumerate(self._progression_futures):
    if self._post_compile_data and future.done():
        # Logic here

# Check invariant conditions before the loop
if self._post_compile_data:
    for i, future in enumerate(self._progression_futures):
        if future.done():
            # Logic here
```

And always use named constants instead of unexplained numbers:
```python
# Instead of:
for i, (gb_type, info) in enumerate(sorted(gb_types.items()), 1001):
    # Logic using magic number 1001

# Use:
START_ID = 1001  # Base ID for graph break types
for i, (gb_type, info) in enumerate(sorted(gb_types.items()), START_ID):
    # Logic using named constant
```