---
title: Prevent memory leaks
description: Always ensure proper memory management when using dynamic allocation.
  Memory leaks are a critical performance issue that can degrade application performance
  over time and eventually lead to resource exhaustion.
repository: deeplearning4j/deeplearning4j
label: Performance Optimization
language: C++
comments_count: 2
repository_stars: 14036
---

Always ensure proper memory management when using dynamic allocation. Memory leaks are a critical performance issue that can degrade application performance over time and eventually lead to resource exhaustion.

Instead of using raw pointers with `new` without corresponding `delete` operations:

1. Prefer smart pointers (std::unique_ptr, std::shared_ptr) to manage object lifetimes automatically
2. Follow RAII (Resource Acquisition Is Initialization) principles
3. If raw pointers must be used, ensure each allocation has a matching deallocation in appropriate cleanup methods

Poor example (potential memory leak):
```cpp
ShapeDescriptor *descriptor = new ShapeDescriptor(dtype, order, shape);
// Missing corresponding delete
```

Better example:
```cpp
// Using smart pointer
std::unique_ptr<ShapeDescriptor> descriptor = 
    std::make_unique<ShapeDescriptor>(dtype, order, shape);
// No explicit delete needed, memory will be freed automatically

// Or if raw pointer is necessary
ShapeDescriptor *descriptor = new ShapeDescriptor(dtype, order, shape);
try {
    // use descriptor
    // ...
    delete descriptor;  // Clean up when done
} catch (...) {
    delete descriptor;  // Clean up on exceptions too
    throw;
}
```