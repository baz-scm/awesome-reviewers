---
title: Avoid redundant calculations
description: 'Eliminate redundant calculations by identifying and caching frequently
  used values to improve performance. Consider these optimization patterns:


  1. Cache function results when used multiple times:'
repository: apache/mxnet
label: Performance Optimization
language: Other
comments_count: 4
repository_stars: 20801
---

Eliminate redundant calculations by identifying and caching frequently used values to improve performance. Consider these optimization patterns:

1. Cache function results when used multiple times:
```cpp
// Before
if (fabs(y) > 1.0) { ... }
// later in the same function
if (fabs(y) < CENTRAL_RANGE) { ... }

// After
double abs_y = fabs(y);
if (abs_y > 1.0) { ... }
// later
if (abs_y < CENTRAL_RANGE) { ... }
```

2. Move repeatedly calculated values to class attributes:
```cpp
// Before - calculating strides in multiple methods
void DNNLSplitFwd::Method1() {
  std::vector<int> strides(ishape.ndim(), 1);
  for (int i = ishape.ndim() - 2; i >= 0; --i) {
    strides[i] = strides[i + 1] * ishape[i + 1];
  }
  // use strides...
}

// After - calculate once and store in class
class DNNLSplitFwd {
  std::vector<int> strides; // Class member
  
  void CalculateStrides() {
    strides.resize(ishape.ndim(), 1);
    for (int i = ishape.ndim() - 2; i >= 0; --i) {
      strides[i] = strides[i + 1] * ishape[i + 1];
    }
  }
};
```

3. When working with containers, prefer `emplace_back` over `push_back` to avoid creating temporary objects:
```cpp
// Before
matched_list.push_back(&n);

// After
matched_list.emplace_back(&n);
```

These optimizations can significantly improve performance in computationally intensive applications by reducing unnecessary calculations, memory operations, and object constructions.
