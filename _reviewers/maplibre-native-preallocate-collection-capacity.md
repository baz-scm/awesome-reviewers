---
title: Preallocate collection capacity
description: When the final size of a collection is known before adding elements,
  use `reserve()` to preallocate memory capacity. This optimization eliminates multiple
  reallocations and copy operations during insertions, improving both performance
  and memory usage patterns. This is particularly beneficial in performance-critical
  code paths where collections are...
repository: maplibre/maplibre-native
label: Performance Optimization
language: C++
comments_count: 4
repository_stars: 1411
---

When the final size of a collection is known before adding elements, use `reserve()` to preallocate memory capacity. This optimization eliminates multiple reallocations and copy operations during insertions, improving both performance and memory usage patterns. This is particularly beneficial in performance-critical code paths where collections are frequently constructed or modified.

```cpp
// Inefficient approach - may cause multiple reallocations
std::vector<AnchorOffsetPair> collection;
for (const auto& anchorOffset : variableAnchorOffset) {
    collection.emplace_back(anchorOffset);
}

// Optimized approach - single allocation
std::vector<AnchorOffsetPair> collection;
collection.reserve(variableAnchorOffset.size());  // Pre-allocate memory
for (const auto& anchorOffset : variableAnchorOffset) {
    collection.emplace_back(anchorOffset);
}
```

Even for small collections, this practice improves code efficiency. For vectors that grow incrementally with push_back or emplace_back operations, each reallocation requires copying all existing elements to a new memory location, which becomes increasingly expensive as the collection grows.