---
title: Type-appropriate null representation
description: Always use type-appropriate mechanisms to represent the absence of a
  value. For objects, use default constructors rather than nullptr. For potentially
  absent values, consider using optional types. For pointers, use null checks before
  performing operations on them.
repository: pytorch/pytorch
label: Null Handling
language: C++
comments_count: 2
repository_stars: 91345
---

Always use type-appropriate mechanisms to represent the absence of a value. For objects, use default constructors rather than nullptr. For potentially absent values, consider using optional types. For pointers, use null checks before performing operations on them.

Examples:
- INCORRECT: `bias_md = nullptr;` when `bias_md` is an object type (dnnl::memory::desc)
- CORRECT: `bias_md = dnnl::memory::desc();` to represent an "empty" descriptor

- INCORRECT: `ncclHeartbeatMonitorThread_ = std::thread(...);` without checking current state
- CORRECT: 
```cpp
// Check nullness before assignment to prevent issues on second call
if (!ncclHeartbeatMonitorThread_.joinable()) {
  ncclHeartbeatMonitorThread_ = std::thread(...);
}
```

This practice improves type safety, prevents null pointer dereferences, and creates more maintainable code by using language features designed for representing absence of values.