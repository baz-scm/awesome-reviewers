---
title: Performance-Sensitive Efficiency
description: 'When optimizing, watch for *hidden* inefficiencies: avoid O(n) per-step
  operations, don’t duplicate expensive work, and don’t eagerly materialize/convert
  data unless needed.'
repository: TheAlgorithms/Python
label: Performance Optimization
language: Python
comments_count: 6
repository_stars: 220912
---

When optimizing, watch for *hidden* inefficiencies: avoid O(n) per-step operations, don’t duplicate expensive work, and don’t eagerly materialize/convert data unless needed.

Apply these checks:
- **Choose linear-time operations for hot loops**: don’t repeatedly shift lists (e.g., `insert(0, ...)`). Prefer build-then-postprocess (append + reverse) when ordering allows.
- **Compute once per candidate/path**: avoid patterns that re-run the same expensive computation in both an `if` and a value/return.
- **Gate expensive transforms**: symbolic simplification (e.g., `sympy.simplify()`) can dominate runtime—make it optional or clearly document the cost.
- **Avoid unnecessary materialization/conversion**: validate input size *before* `map()`/list creation; don’t re-wrap inputs already in the expected type (e.g., `np.array(arr)` when `arr` is already `np.ndarray`).
- **Avoid double iteration**: combine validation with the main loop when that removes an extra pass.

Example patterns (correct-by-construction + faster):
```python
# 1) Avoid insert-at-front in recursion: use append + reverse
result = []
# ... DFS fills `result` with descendants-first
return list(reversed(result))

# 2) Compute expensive support once
candidate_counts = {}
for c in candidates:
    support = get_support(c, transactions)
    if support >= min_support:
        candidate_counts[c] = support

# 3) Check length before mapping
tokens = input().split()
if len(tokens) > MAX_SEQUENCE_LENGTH:
    ...
user_input = list(map(int, tokens))

# 4) Optional expensive simplify
def maybe_simplify(expr, *, simplify: bool = False):
    return sp.simplify(expr) if simplify else expr

# 5) Avoid redundant conversion
if not isinstance(arr, np.ndarray):
    arr = np.array(arr)
```