---
title: Use named constants
description: In AI model implementations, avoid using magic numbers directly in code
  as they reduce readability and make maintenance difficult. Always define constants
  with meaningful names, especially for values related to tensor dimensions, indices,
  and type identifiers.
repository: apache/mxnet
label: AI
language: Other
comments_count: 2
repository_stars: 20801
---

In AI model implementations, avoid using magic numbers directly in code as they reduce readability and make maintenance difficult. Always define constants with meaningful names, especially for values related to tensor dimensions, indices, and type identifiers.

For dimension limits:
```cpp
// Instead of this:
if (shape.ndim() >= 1 && shape.ndim() <= 12) {
  // Process shape
}

// Use this:
const int MAX_ONEDNN_DIMS = 12;
if (shape.ndim() >= 1 && shape.ndim() <= MAX_ONEDNN_DIMS) {
  // Process shape
}
```

For array indices representing specific tensor components:
```cpp
// Instead of this:
if (n->inputs[2].node->is_variable()) {
  // Process bias
}

// Use this:
const int BIAS_INDEX = 2;  // Or better, use enum or named constant
if (n->inputs[BIAS_INDEX].node->is_variable()) {
  // Process bias
}
```

This practice makes code more maintainable as dimensions and tensor layouts evolve during AI model optimization efforts.
