---
title: protect shared data
description: Always protect shared data that can be accessed by multiple threads using
  appropriate synchronization mechanisms. Identify potential race conditions where
  shared state could be modified concurrently and choose the right protection mechanism.
repository: llvm/llvm-project
label: Concurrency
language: C++
comments_count: 2
repository_stars: 33702
---

Always protect shared data that can be accessed by multiple threads using appropriate synchronization mechanisms. Identify potential race conditions where shared state could be modified concurrently and choose the right protection mechanism.

For simple data that needs atomic updates, use atomic operations:
```cpp
// TODO: needs a mutex
// Better: use atomic for simple counters/flags
std::atomic<int> shared_counter{0};
```

For complex shared state or when you need to protect critical sections, use mutexes:
```cpp
// Protect complex operations on shared data
std::mutex data_mutex;
void update_shared_state() {
    std::lock_guard<std::mutex> lock(data_mutex);
    // Critical section - modify shared data safely
}
```

Be especially careful with global variables that have external linkage, as they can be modified by other compilation units, breaking thread safety assumptions. Consider using `static` linkage or proper synchronization:
```cpp
// Problematic: global linkage allows external modification
const int SHARED_CONSTANT = -1;

// Better: static linkage prevents external access
static const int SHARED_CONSTANT = -1;
// Or: use proper synchronization for truly shared data
```

When reviewing code, look for shared mutable state and verify it has appropriate protection against concurrent access.