---
title: Choose appropriate pointer types
description: 'Select the right pointer type based on ownership semantics to prevent
  null reference issues and memory leaks. Follow these guidelines:


  1. Use smart pointers (`shared_ptr`, `unique_ptr`) when ownership transfer is needed'
repository: pytorch/pytorch
label: Null Handling
language: Other
comments_count: 2
repository_stars: 91345
---

Select the right pointer type based on ownership semantics to prevent null reference issues and memory leaks. Follow these guidelines:

1. Use smart pointers (`shared_ptr`, `unique_ptr`) when ownership transfer is needed
2. Use `weak_ptr` for non-owning references to shared objects to avoid cyclic dependencies
3. Raw pointers are appropriate only when the object's lifetime is guaranteed to exceed the pointer's usage

Be explicit about object lifecycle by properly defining or deleting special member functions in classes that manage resources.

```cpp
// GOOD: Clear ownership with smart pointer
std::unique_ptr<HeartbeatMonitor> monitor_ = std::make_unique<HeartbeatMonitor>();

// GOOD: Non-owning reference to shared object, avoids cyclic dependency
std::weak_ptr<ProcessGroupNCCL> processGroup_;

// ACCEPTABLE: Raw pointer when lifecycle is contained within parent
// HeartbeatMonitor(ProcessGroupNCCL* pg); // Only if pg's lifetime > HeartbeatMonitor

// GOOD: Explicitly handle or delete copy semantics to prevent null reference issues
struct MPSCachedKernel {
  MPSCachedKernel(NSObject* object) : _object([object retain]) {}
  MPSCachedKernel(const MPSCachedKernel&) = delete; // Prevent accidental copies
  // ...
};
```