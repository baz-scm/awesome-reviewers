---
title: validate algorithm boundaries
description: Always validate boundary conditions and termination criteria in algorithms
  to prevent infinite loops, out-of-bounds access, and incorrect behavior. This includes
  checking loop bounds against variable type limits, validating range parameters,
  and ensuring proper termination conditions.
repository: tree-sitter/tree-sitter
label: Algorithms
language: C
comments_count: 4
repository_stars: 21799
---

Always validate boundary conditions and termination criteria in algorithms to prevent infinite loops, out-of-bounds access, and incorrect behavior. This includes checking loop bounds against variable type limits, validating range parameters, and ensuring proper termination conditions.

Key practices:
- Add explicit bounds checking when loop variables might exceed their type limits
- Validate range parameters using appropriate logical operators (OR for exclusion, AND for inclusion)
- Check boundary conditions before performing expensive operations like recursive searches
- Use proper comparison operators that account for edge cases like empty ranges

Example from loop bounds checking:
```c
// Problem: infinite loop if count > UINT16_MAX
for (TSSymbol i = 0; i < count; i++) { ... }

// Solution: add explicit bounds check
for (TSSymbol i = 0; i < count && i < UINT16_MAX; i++) { ... }
```

Example from range validation:
```c
// Problem: incorrect logic for range exclusion
if (end_byte <= start_byte && point_lte(end_point, start_point)) { ... }

// Solution: use OR for exclusion checks
bool node_precedes_range = (
  ts_node_end_byte(node) <= self->start_byte ||
  point_lte(ts_node_end_point(node), self->start_point)
);
```

Proper boundary validation prevents algorithmic failures and improves both correctness and performance by avoiding unnecessary computation on invalid inputs.