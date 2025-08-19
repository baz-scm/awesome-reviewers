---
title: prefer simple optimizations
description: When implementing performance optimizations, favor simple, straightforward
  approaches over complex solutions unless the complexity is clearly justified by
  significant performance gains. Complex optimizations often introduce maintenance
  burden, reduce code readability, and may not provide proportional benefits.
repository: ClickHouse/ClickHouse
label: Performance Optimization
language: Other
comments_count: 3
repository_stars: 42425
---

When implementing performance optimizations, favor simple, straightforward approaches over complex solutions unless the complexity is clearly justified by significant performance gains. Complex optimizations often introduce maintenance burden, reduce code readability, and may not provide proportional benefits.

Before implementing a complex optimization:
1. Try the simplest approach first and measure its impact
2. Only add complexity if simple solutions are insufficient
3. Document why the complexity is necessary

Example of preferred simple approach:
```cpp
// Simple prefetching - preferred
if (prefetch_ahead > 0) {
    __builtin_prefetch(current + prefetch_ahead);
}

// Instead of complex ring buffer implementation
```

Example of keeping codec selection simple:
```cpp
// Prefer portable, simple codec selection
static constexpr auto CODEC_NAME = "simdfastpfor128";
static constexpr size_t THRESHOLD = 4;

// Instead of complex compile-time CPU feature detection
```

This approach reduces the risk of introducing bugs in performance-critical code while maintaining the primary performance benefits. Complex optimizations should be reserved for cases where profiling clearly demonstrates that simple approaches are insufficient and the performance gain justifies the added complexity.