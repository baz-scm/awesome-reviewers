---
title: Cache expensive computations
description: Identify and cache the results of expensive computations to avoid redundant
  calculations, especially in performance-critical code paths. This includes recursive
  functions, user-defined callbacks, and complex arithmetic operations that may be
  called multiple times with the same inputs.
repository: facebook/yoga
label: Performance Optimization
language: C++
comments_count: 2
repository_stars: 18255
---

Identify and cache the results of expensive computations to avoid redundant calculations, especially in performance-critical code paths. This includes recursive functions, user-defined callbacks, and complex arithmetic operations that may be called multiple times with the same inputs.

When reviewing code, look for:
- Repeated calls to expensive functions like recursive calculations or user callbacks
- Complex arithmetic operations that could be simplified or pre-computed
- Opportunities to store intermediate results for reuse

Example of caching expensive baseline calculations:
```cpp
// Before: Calling YGBaseline multiple times
if (alignItem == YGAlignBaseline) {
  leadingCrossDim += collectedFlexItemsValues.maxBaselineAscent - YGBaseline(child);
}
// Later in code...
someOtherValue = YGBaseline(child); // Redundant call

// After: Cache the result in child layout
// At algorithm start: child->getLayout().cachedBaseline = YGBaseline(child);
if (alignItem == YGAlignBaseline) {
  leadingCrossDim += collectedFlexItemsValues.maxBaselineAscent - child->getLayout().cachedBaseline;
}
```

This optimization is particularly important for functions that are recursive, call user-defined callbacks, or are executed in tight loops where performance matters most.