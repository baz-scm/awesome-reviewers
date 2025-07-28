---
title: Eliminate unnecessary computations
description: Identify and remove redundant operations, unnecessary copies, and repeated
  computations that add algorithmic overhead without providing value. This includes
  avoiding redundant hash operations, using const references instead of copies, implementing
  memoization for expensive lookups, and making conscious space-time tradeoffs.
repository: facebook/react-native
label: Algorithms
language: Other
comments_count: 4
repository_stars: 123178
---

Identify and remove redundant operations, unnecessary copies, and repeated computations that add algorithmic overhead without providing value. This includes avoiding redundant hash operations, using const references instead of copies, implementing memoization for expensive lookups, and making conscious space-time tradeoffs.

Key patterns to watch for:
- Hash functions that perform unnecessary operations (e.g., `hash_combine` with seed 0 instead of returning the hash directly)
- Using `auto` instead of `const auto&` when working with existing objects, causing unnecessary copies
- Repeated expensive operations like `NSClassFromString` that can be cached with static variables
- Storing precomputed state vs recomputing on-demand based on access patterns

Example optimization:
```cpp
// Instead of redundant hash_combine:
facebook::react::hash_combine(seed, color.getUIColorHash());

// Return hash directly:
return color.getUIColorHash();

// Use const references to avoid copies:
const auto& orientation = gradient.orientation;
const auto& colorStops = gradient.colorStops;
```

Consider the frequency of operations and choose the approach that minimizes total computational cost while maintaining code clarity.