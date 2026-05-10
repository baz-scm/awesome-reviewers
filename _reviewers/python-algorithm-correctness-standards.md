---
title: Algorithm Correctness Standards
description: 'When implementing algorithms, enforce correctness and reliability by
  following this checklist:


  1) Validate stated preconditions (and document them)

  - If the algorithm only works for certain input ranges/shapes (e.g., cyclic sort
  requires values in 1..n with no duplicates), explicitly check those conditions and
  fail fast with a clear error.'
repository: TheAlgorithms/Python
label: Algorithms
language: Python
comments_count: 6
repository_stars: 220912
---

When implementing algorithms, enforce correctness and reliability by following this checklist:

1) Validate stated preconditions (and document them)
- If the algorithm only works for certain input ranges/shapes (e.g., cyclic sort requires values in 1..n with no duplicates), explicitly check those conditions and fail fast with a clear error.

2) Handle numerical/semantic edge cases explicitly
- For floating-point boundary conditions, use `math.isclose()` (and/or symmetric checks) instead of direct comparisons.
- For floating-point pivot/zero checks, use a tolerance rather than `== 0.0`.

3) Ensure algorithm invariants are implemented (especially graph/search)
- If the correctness relies on traversal order (e.g., DFS post-order), apply required transformations (`reverse()`) and add a brief comment explaining why.

4) Avoid unnecessary extra passes
- Prefer single-pass grouping/processing over multiple full iterations when the same data can be grouped in one traversal.

Example pattern (single-pass grouping + clear precondition validation):
```python
from collections import defaultdict

def group_by_priority(items: list[dict]) -> dict[str, list[dict]]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for item in items:
        grouped[item["priority"]].append(item)
    return dict(grouped)

def cyclic_sort_guard(nums: list[int]) -> None:
    n = len(nums)
    if any(x < 1 or x > n for x in nums):
        raise ValueError("Cyclic sort requires all values in the range [1, len(nums)]")
    if len(set(nums)) != n:
        raise ValueError("Cyclic sort requires no duplicates")
```

Adopting this standard will reduce subtle correctness bugs (wrong logic/invariants), runtime failures (invalid inputs/infinite loops), and precision-related issues, while also improving efficiency for larger inputs.