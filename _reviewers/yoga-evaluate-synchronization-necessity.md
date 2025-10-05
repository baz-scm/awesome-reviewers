---
title: Evaluate synchronization necessity
description: Before implementing thread safety mechanisms like atomic operations or
  mutexes for global variables, critically assess whether perfect synchronization
  is actually required for program correctness. Consider the performance cost of synchronization
  against the importance of data accuracy.
repository: facebook/yoga
label: Concurrency
language: C++
comments_count: 4
repository_stars: 18255
---

Before implementing thread safety mechanisms like atomic operations or mutexes for global variables, critically assess whether perfect synchronization is actually required for program correctness. Consider the performance cost of synchronization against the importance of data accuracy.

Many global variables, especially counters or flags, may not require strict synchronization if approximate or eventually consistent values are sufficient for the use case. For example, instance counters used only for testing or debugging may not justify the synchronization overhead.

Example of unnecessary synchronization:
```cpp
// Before: Adding atomic for test-only counter
std::atomic<int32_t> gNodeInstanceCount(0);  // Causes bus overhead

// After: Conditional compilation or accepting approximate values
#ifdef YOGA_TESTING
int32_t gNodeInstanceCount = 0;  // Only precise in single-threaded tests
#endif
```

Example of questioning atomic necessity:
```cpp
// Before: Automatic atomic usage
std::atomic<uint8_t> gCurrentGenerationCount{0};

// Consider: Does increment accuracy matter?
// If the purpose is just to invalidate caches and trigger recalculations,
// occasional missed increments may be acceptable and avoid synchronization costs
uint8_t gCurrentGenerationCount = 0;  // Simple increment, accepts race conditions
```

Key evaluation criteria:
1. Is perfect accuracy required for correctness?
2. What is the performance impact of synchronization?
3. Can the system tolerate approximate or eventually consistent values?
4. Are there alternative designs that avoid shared state entirely?

This approach prevents over-engineering thread safety solutions and maintains better performance in concurrent systems.