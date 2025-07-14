---
title: Reuse computed values efficiently
description: Move variable declarations and computations outside of loops when their
  values don't change between iterations. This reduces memory allocations and avoids
  redundant computations, improving performance.
repository: nodejs/node
label: Performance Optimization
language: Other
comments_count: 3
repository_stars: 112178
---

Move variable declarations and computations outside of loops when their values don't change between iterations. This reduces memory allocations and avoids redundant computations, improving performance.

Example - Before:
```cpp
for (const auto& resource_entry : manager->held_locks_) {
  for (const auto& held_lock : resource_entry.second) {
    Local<Object> lock_info = CreateLockInfoObject(...);
    // Use lock_info
  }
}
```

Example - After:
```cpp
Local<Object> lock_info;
for (const auto& resource_entry : manager->held_locks_) {
  for (const auto& held_lock : resource_entry.second) {
    lock_info = CreateLockInfoObject(...);
    // Use lock_info
  }
}
```

Similarly, cache computed values that are used repeatedly:
```cpp
// Before: Computing in every call
std::string normalised_cache_dir = NormalisePath(cache_dir);

// After: Store as member variable
class CompileCacheHandler {
  std::string normalised_cache_dir_;
  // Compute once in constructor
};
```