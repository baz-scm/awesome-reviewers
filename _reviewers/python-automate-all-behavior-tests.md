---
title: Automate All Behavior Tests
description: 'For every algorithmic change (and every public function/class), require
  automated tests that lock in both correctness and failure modes.


  Minimum standard:'
repository: TheAlgorithms/Python
label: Testing
language: Python
comments_count: 10
repository_stars: 220912
---

For every algorithmic change (and every public function/class), require automated tests that lock in both correctness and failure modes.

Minimum standard:
- Prefer assertions/doctests over “print and eyeball.” (Printing-only checks are not sufficient.)
- Add doctests or pytest cases for: 
  - happy path(s)
  - edge cases (empty input, boundaries, negative values, single element)
  - invalid inputs / rejected preconditions (at least one case that should fail or return a sentinel)
- Don’t weaken confidence with tests that all assert the same output for different inputs—add cases that meaningfully differ.
- Keep existing tests; don’t remove doctests “just because.”
- Ensure doctests actually execute in the module (e.g., call `doctest.testmod()` in `__main__`).
- Avoid nested helper functions when you rely on doctest coverage inside their docstrings; keep testable code at module level.

Example pattern (doctest with edge + failure):
```python
def interpolation_search(sorted_collection: list[int], item: int) -> int | None:
    """
    >>> interpolation_search([1, 2, 3, 4, 5], 2)
    1
    >>> interpolation_search([1, 2, 3, 4, 5], 6) is None
    True
    >>> interpolation_search([], 1) is None
    True
    """
    ...

if __name__ == "__main__":
    import doctest
    doctest.testmod()
```

This standard directly prevents regressions (new validation rules, edge-case fixes, and invariants) and makes behavior verification repeatable and reviewable.