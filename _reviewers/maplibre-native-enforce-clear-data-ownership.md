---
title: Enforce clear data ownership
description: 'Always establish and maintain clear ownership semantics in concurrent
  code to prevent data races. This includes:


  1. Use RAII patterns for resource management (especially locks)'
repository: maplibre/maplibre-native
label: Concurrency
language: C++
comments_count: 4
repository_stars: 1411
---

Always establish and maintain clear ownership semantics in concurrent code to prevent data races. This includes:

1. Use RAII patterns for resource management (especially locks)
2. Ensure data lifetime matches synchronization scope
3. Prefer value semantics over references for shared data
4. Be explicit about ownership transfer in async operations

Example of proper RAII lock usage:
```cpp
void DynamicTexture::reserveSize(const Size& size, int32_t uniqueId) {
    std::lock_guard<std::mutex> guard(mutex); // RAII lock
    // ... protected operations ...
} // Auto-unlock on scope exit

// Instead of:
void DynamicTexture::reserveSize(const Size& size, int32_t uniqueId) {
    mutex.lock();
    // ... operations that might throw ...
    mutex.unlock(); // Might never be reached!
}
```

For shared data access:
```cpp
// Avoid:
std::string_view getData() {
    std::shared_lock<std::shared_mutex> lock(mutex);
    return string_view{buffer.data()}; // Dangerous! View might outlive lock
}

// Prefer:
std::string getData() {
    std::shared_lock<std::shared_mutex> lock(mutex);
    return std::string{buffer}; // Safe copy
}
```