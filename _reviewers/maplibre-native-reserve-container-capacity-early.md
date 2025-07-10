---
title: Reserve container capacity early
description: When using containers like `unordered_map`, `unordered_set`, or vectors
  in performance-critical code, always pre-allocate space by calling `reserve()` before
  adding elements. This prevents expensive rehashing or reallocation operations during
  insertion, which can cause significant performance degradation, especially in rendering
  loops or frequently called...
repository: maplibre/maplibre-native
label: Performance Optimization
language: Other
comments_count: 3
repository_stars: 1411
---

When using containers like `unordered_map`, `unordered_set`, or vectors in performance-critical code, always pre-allocate space by calling `reserve()` before adding elements. This prevents expensive rehashing or reallocation operations during insertion, which can cause significant performance degradation, especially in rendering loops or frequently called functions.

For string-heavy lookups and comparisons, consider using specialized containers like `StringIndexer` with `unordered_set<StringIdentity>` instead of storing and comparing raw strings directly.

Example:
```cpp
// Suboptimal: May cause multiple reallocations
std::unordered_map<TextureID, TextureDesc> textureMap;
// Add many elements...

// Better: Pre-allocate expected capacity
std::unordered_map<TextureID, TextureDesc> textureMap;
textureMap.reserve(expectedCount); // Prevent rehashing during insertion
// Add many elements...

// Even better for string comparisons in hot paths:
std::unordered_set<StringIdentity> propertiesAsUniforms;
propertiesAsUniforms.reserve(expectedPropertyCount);
// This optimization can help with performance in methods called per frame
```

This simple practice can significantly reduce memory allocation overhead, especially in data structures accessed in rendering loops or hot paths in your graphics code.