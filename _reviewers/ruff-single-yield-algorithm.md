---
title: Single yield algorithm
description: 'Context managers must follow a crucial algorithmic constraint: each
  execution path must yield exactly once. Multiple yields in the same path lead to
  unpredictable behavior, while no yields prevent proper resource management.'
repository: astral-sh/ruff
label: Algorithms
language: Python
comments_count: 2
repository_stars: 40619
---

Context managers must follow a crucial algorithmic constraint: each execution path must yield exactly once. Multiple yields in the same path lead to unpredictable behavior, while no yields prevent proper resource management.

When implementing context managers with `@contextlib.contextmanager`:

1. Ensure mutually exclusive branches if using conditional yields
2. Use early returns to prevent execution of subsequent yields
3. Avoid yields in loops or anywhere that could lead to multiple yields during execution

Example of correct implementation:
```python
@contextlib.contextmanager
def valid_context_manager(condition):
    # Setup code
    try:
        if condition:
            yield "success"
            return  # Early return prevents reaching the next yield
        yield "alternative"
    finally:
        # Cleanup code always executed
        print("Cleaning up")
```

This pattern ensures the algorithm's invariant of "yield exactly once" regardless of which execution path is taken, maintaining reliable resource acquisition and release.