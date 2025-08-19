---
title: Protect shared state
description: Always protect shared mutable state with appropriate synchronization
  mechanisms to prevent race conditions and data corruption in multi-threaded environments.
  Use `std::call_once` for thread-safe initialization, mutexes for protecting shared
  resources, and carefully consider whether state belongs in global vs local thread
  contexts.
repository: duckdb/duckdb
label: Concurrency
language: C++
comments_count: 4
repository_stars: 32061
---

Always protect shared mutable state with appropriate synchronization mechanisms to prevent race conditions and data corruption in multi-threaded environments. Use `std::call_once` for thread-safe initialization, mutexes for protecting shared resources, and carefully consider whether state belongs in global vs local thread contexts.

Key practices:
- Use `std::call_once` instead of simple boolean flags for one-time initialization
- Wrap shared resources like static variables with mutex protection
- Place ordinality counters and similar sequential data in global state with proper locking when multiple threads need coordinated access
- Avoid placing thread-coordination data in local state when parallel execution is expected

Example of proper initialization:
```cpp
void KeywordHelper::InitializeKeywordMaps() {
    static std::once_flag initialized_flag;
    std::call_once(initialized_flag, []() {
        // initialization code here
    });
}
```

Example of protecting shared output:
```cpp
struct FailureSummary {
    void AddSummary(const string &failure) {
        std::lock_guard<std::mutex> guard(lock);
        summary << failure;
    }
    std::ostringstream summary;
    std::mutex lock;
};
```

When designing parallel operators, ensure that shared sequential state (like ordinality indices) is properly synchronized in global state rather than duplicated in local thread state, which would produce incorrect results across parallel execution paths.