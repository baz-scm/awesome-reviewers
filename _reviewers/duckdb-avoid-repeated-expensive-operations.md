---
title: avoid repeated expensive operations
description: Identify and eliminate repeated expensive computations, especially in
  loops and frequently executed code paths. This optimization principle focuses on
  moving invariant calculations outside loops, caching results of expensive operations,
  and avoiding unnecessary data conversions or memory allocations.
repository: duckdb/duckdb
label: Performance Optimization
language: C++
comments_count: 7
repository_stars: 32061
---

Identify and eliminate repeated expensive computations, especially in loops and frequently executed code paths. This optimization principle focuses on moving invariant calculations outside loops, caching results of expensive operations, and avoiding unnecessary data conversions or memory allocations.

Key strategies include:

1. **Move loop-invariant operations outside loops**: Instead of performing the same expensive computation in every iteration, calculate it once before the loop starts.

```cpp
// Instead of this:
for (idx_t child_idx = 0; child_idx < entry.length; child_idx++) {
    if (actual_value == ((T *)value_data.data)[0]) { // Repeated casting
        // ...
    }
}

// Do this:
auto values = (T *)value_data.data; // Cast once outside loop
for (idx_t child_idx = 0; child_idx < entry.length; child_idx++) {
    if (actual_value == values[0]) {
        // ...
    }
}
```

2. **Cache expensive expression evaluations**: If an expression can be folded or has `IsFoldable()`, cache the result to avoid repeated evaluation in performance-critical paths.

3. **Avoid unnecessary string conversions and copies**: Use direct data access methods like `StringUtil::CIEquals` on `string_t` data instead of creating temporary string copies for comparisons.

4. **Optimize early exit conditions**: Move null checks and other early termination conditions to the beginning of loops to avoid wasting computation on data that will be discarded.

This principle is particularly important in database query execution, aggregation functions, and data processing pipelines where the same operations may be performed millions of times.