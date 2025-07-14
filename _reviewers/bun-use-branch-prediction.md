---
title: Use branch prediction
description: Optimize performance-critical algorithms by using branch prediction hints
  to guide the CPU. Add `UNLIKELY` macros for error conditions, boundary checks, or
  exceptional cases that rarely evaluate to true, and `LIKELY` for common execution
  paths. This helps the CPU's branch predictor make better decisions, reducing pipeline
  stalls and improving execution...
repository: oven-sh/bun
label: Algorithms
language: C++
comments_count: 2
repository_stars: 79093
---

Optimize performance-critical algorithms by using branch prediction hints to guide the CPU. Add `UNLIKELY` macros for error conditions, boundary checks, or exceptional cases that rarely evaluate to true, and `LIKELY` for common execution paths. This helps the CPU's branch predictor make better decisions, reducing pipeline stalls and improving execution speed in hot loops and frequently called functions.

Example:
```cpp
// Less optimized:
if (number_num < lower_num || number_num > upper_num) {
    // Handle out-of-range case
}

// Optimized with branch prediction:
if (UNLIKELY(number_num < lower_num || number_num > upper_num)) {
    // Handle out-of-range case
}
```

This technique is especially important in performance-critical algorithms where the same conditional is evaluated repeatedly and the outcome is predictable in most cases.