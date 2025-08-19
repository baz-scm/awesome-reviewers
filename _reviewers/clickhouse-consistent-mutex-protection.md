---
title: consistent mutex protection
description: Ensure consistent mutex usage across all access points to shared data
  structures and clearly document what each mutex protects. Inconsistent locking can
  lead to race conditions, data corruption, and crashes.
repository: ClickHouse/ClickHouse
label: Concurrency
language: C++
comments_count: 2
repository_stars: 42425
---

Ensure consistent mutex usage across all access points to shared data structures and clearly document what each mutex protects. Inconsistent locking can lead to race conditions, data corruption, and crashes.

Key principles:
1. **Use the same mutex** for all operations on a shared data structure - don't mix different mutexes for the same resource
2. **Document protection boundaries** clearly, ideally with Thread Safety Analysis (TSA) annotations
3. **Prefer `std::lock_guard`** over `std::scoped_lock` for single mutex scenarios
4. **Structure code to minimize lock scope** and avoid accessing potentially unsafe pointers outside critical sections

Example of problematic inconsistent locking:
```cpp
// BAD: Different mutexes protecting the same data
std::mutex mutex;
std::shared_mutex shared_mutex;
std::unordered_map<int32_t, HandlerInfo> functionIdToHandlers;

void setHandler() {
    std::lock_guard<std::mutex> lock(mutex);  // Uses mutex
    functionIdToHandlers[id] = handler;
}

void dispatchHandler() {
    std::shared_lock lock(shared_mutex);  // Uses shared_mutex!
    auto it = functionIdToHandlers.find(id);  // Race condition!
}

void processHandler() {
    // No lock at all - definitely unsafe!
    functionIdToHandlers[id].process();
}
```

Better approach with consistent protection:
```cpp
// GOOD: Single mutex with clear scope
std::shared_mutex handlers_mutex;  // Clearly named
std::unordered_map<int32_t, HandlerInfo> functionIdToHandlers GUARDED_BY(handlers_mutex);

void setHandler() {
    std::lock_guard lock(handlers_mutex);
    functionIdToHandlers[id] = handler;
}

void dispatchHandler() {
    HandlerInfo handler_copy;
    {
        std::shared_lock lock(handlers_mutex);
        auto it = functionIdToHandlers.find(id);
        if (it != functionIdToHandlers.end()) {
            handler_copy = it->second;  // Copy under lock
        }
    }
    // Use handler_copy safely outside lock
    if (handler_copy.isValid()) {
        handler_copy.process();
    }
}
```

This prevents race conditions where concurrent modifications can invalidate iterators or cause undefined behavior during map resizing.