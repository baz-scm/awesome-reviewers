---
title: Optimize container operations
description: 'Minimize CPU overhead in container operations by using efficient data
  structure patterns:


  1. **Use static containers** for fixed lookup tables or maps that are frequently
  accessed but rarely changed. This avoids reconstruction overhead on each function
  call:'
repository: pytorch/pytorch
label: Performance Optimization
language: Other
comments_count: 2
repository_stars: 91345
---

Minimize CPU overhead in container operations by using efficient data structure patterns:

1. **Use static containers** for fixed lookup tables or maps that are frequently accessed but rarely changed. This avoids reconstruction overhead on each function call:
```cpp
// Inefficient: Recreates map on every function call
void handle() {
    std::unordered_map<int, HandlerFn> handler_map = { /* entries */ };
    // ...
}

// Efficient: Creates map once for all calls
void handle() {
    static std::unordered_map<int, HandlerFn> handler_map = { /* entries */ };
    // ...
}
```

2. **Prefer emplace over insert** for maps and other containers to avoid unnecessary temporary object construction:
```cpp
// Less efficient: Creates a temporary pair object
args.insert({DNNL_ARG_SRC, dnnl::memory(m1_md, eng, m1.data_ptr())});

// More efficient: Constructs the object in-place
args.emplace(DNNL_ARG_SRC, dnnl::memory(m1_md, eng, m1.data_ptr()));
```

These optimizations reduce memory allocations, minimize CPU cycles, and can significantly improve performance in hot code paths or when working with large containers.