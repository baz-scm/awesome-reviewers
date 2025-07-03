---
title: Optimize memory allocation patterns
description: 'Prefer efficient memory allocation patterns to improve performance.
  Key practices:


  1. Use RAII containers (like Mat) instead of raw pointers to prevent memory leaks'
repository: opencv/opencv
label: Performance Optimization
language: C++
comments_count: 5
repository_stars: 82865
---

Prefer efficient memory allocation patterns to improve performance. Key practices:

1. Use RAII containers (like Mat) instead of raw pointers to prevent memory leaks
2. Pre-allocate containers when size is known
3. Use stack allocation for small, fixed-size objects
4. Avoid unnecessary dynamic allocation

Example - Before:
```cpp
// Inefficient allocation patterns
char* get_raw_data() {
    return new char[size];  // Raw pointer, potential memory leak
}

std::vector<Mat> img_vec;
img_vec.push_back(img);  // Potential reallocation

fcvPyramidLevel_v2 *framePyr = new fcvPyramidLevel_v2[2];  // Unnecessary heap allocation
```

Example - After:
```cpp
// Efficient allocation patterns
Mat get_data() {
    return Mat(size);  // RAII handles cleanup
}

std::vector<Mat> img_vec(1, img);  // Pre-allocated size

fcvPyramidLevel_v2 framePyr[2];  // Stack allocation for small arrays
```

Benefits:
- Prevents memory leaks
- Reduces allocation overhead
- Improves cache utilization
- More predictable performance
