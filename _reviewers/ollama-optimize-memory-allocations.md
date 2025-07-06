---
title: Optimize memory allocations
description: 'Be strategic about memory allocations to improve performance in your
  C++ code. Consider two key optimization patterns:


  1. **Pre-reserve container capacity**: When using containers like vectors that will
  grow to a predictable size, use `reserve()` with a reasonable initial capacity to
  reduce allocation overhead. This prevents multiple small reallocations as...'
repository: ollama/ollama
label: Performance Optimization
language: C++
comments_count: 2
repository_stars: 145705
---

Be strategic about memory allocations to improve performance in your C++ code. Consider two key optimization patterns:

1. **Pre-reserve container capacity**: When using containers like vectors that will grow to a predictable size, use `reserve()` with a reasonable initial capacity to reduce allocation overhead. This prevents multiple small reallocations as the container grows.

```cpp
// Before - May cause multiple reallocations during population
vec_rules[i].resize(n_rules);  

// After - Pre-allocate with reasonable capacity
vec_rules[i].reserve(16);  // Start with reasonable capacity
```

2. **Avoid unnecessary preallocation**: When designing functions that return variable-sized data, prefer return values over output parameters when the required size is difficult to predict in advance. This eliminates the need for callers to pre-allocate buffers of the correct size.

```cpp
// Before - Requires caller to pre-allocate buffer of correct size
int schema_to_grammar(const char *json_schema, char *grammar, size_t max_len);

// After - Return value approach avoids pre-allocation issues
std::string schema_to_grammar(const char *json_schema);
```

Both strategies help minimize memory churn, reduce fragmentation, and improve overall application performance, particularly in performance-critical code paths.