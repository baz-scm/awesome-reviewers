---
title: avoid redundant cache lookups
description: When implementing cache functionality, avoid performing the same cache
  lookup multiple times. Instead, store and reuse the result from the first lookup
  to improve performance.
repository: ClickHouse/ClickHouse
label: Caching
language: C++
comments_count: 2
repository_stars: 42425
---

When implementing cache functionality, avoid performing the same cache lookup multiple times. Instead, store and reuse the result from the first lookup to improve performance.

This is particularly important in scenarios where you need to check if content is cached (e.g., in `isContentCached`) and then immediately perform the actual cache operation (e.g., in `nextImpl`). Rather than doing separate `contains()` and `getOrSet()` calls, perform `getOrSet()` once and store the result for subsequent use.

Example approach:
```cpp
// Instead of checking cache twice:
bool isContentCached(size_t offset, size_t size) {
    return cache->contains(key);  // First lookup
}
bool nextImpl() {
    auto result = cache->getOrSet(key, ...);  // Second lookup
}

// Store the result from first lookup:
bool isContentCached(size_t offset, size_t size) {
    cached_result = cache->getOrSet(key, ...);  // Single lookup, store result
    return cached_result != nullptr;
}
bool nextImpl() {
    // Reuse cached_result instead of looking up again
}
```

This pattern reduces cache overhead and improves overall system performance, especially in high-throughput scenarios where cache operations are frequent.