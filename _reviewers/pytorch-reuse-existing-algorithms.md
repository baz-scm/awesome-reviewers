---
title: Reuse existing algorithms
description: Before implementing common algorithms or utilities, check if the codebase
  already contains an appropriate implementation. Reusing existing, tested code reduces
  bugs, improves maintainability, and often provides better performance characteristics.
repository: pytorch/pytorch
label: Algorithms
language: C++
comments_count: 2
repository_stars: 91345
---

Before implementing common algorithms or utilities, check if the codebase already contains an appropriate implementation. Reusing existing, tested code reduces bugs, improves maintainability, and often provides better performance characteristics.

For example, instead of reimplementing a counting function:

```cpp
// Don't reimplement existing functionality
template <typename T>
size_t count_leading_zeros(T val) {
  // Custom implementation...
}
```

Use the existing implementation:

```cpp
// Do use existing implementations
#include <c10/util/llvmMathExtras.h>
// Then use LeadingZerosCounter directly
```

Similarly, when selecting algorithms (like random number generators), evaluate existing options based on required properties such as period length or performance characteristics. For instance, prefer `VSL_BRNG_PHILOX4X32X10` or `VSL_BRNG_MT19937` over simpler generators if statistical quality is important, rather than implementing custom variants.

This principle helps maintain code consistency, avoids duplication of effort, and leverages optimizations already present in established implementations.