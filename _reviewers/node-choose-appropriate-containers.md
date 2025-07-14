---
title: Choose appropriate containers
description: Select data structures based on expected collection size and usage patterns.
  For small collections (typically fewer than 30 elements), consider using ordered
  containers like `std::map` instead of hash-based ones like `std::unordered_map`.
  With small collections, the theoretical O(log n) vs O(1) lookup time difference
  becomes negligible in practice, while...
repository: nodejs/node
label: Algorithms
language: Other
comments_count: 2
repository_stars: 112178
---

Select data structures based on expected collection size and usage patterns. For small collections (typically fewer than 30 elements), consider using ordered containers like `std::map` instead of hash-based ones like `std::unordered_map`. With small collections, the theoretical O(log n) vs O(1) lookup time difference becomes negligible in practice, while ordered containers avoid hash function computation overhead and potential collision handling.

```cpp
// Instead of using unordered_map for small collections:
std::unordered_map<ModuleRequest, ModuleWrap*> module_requests;

// Consider using an ordered map:
std::map<ModuleRequest, ModuleWrap*> module_requests;
```

When working with hash-based containers, reuse precomputed hash values when available (like V8's `GetIdentityHash()`) instead of recomputing hashes with `std::hash`. This avoids unnecessary computation and improves performance, especially for string data that might already have an identity hash from the JavaScript engine.