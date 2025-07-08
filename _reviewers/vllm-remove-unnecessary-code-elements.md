---
title: Remove unnecessary code elements
description: 'Keep code clean and maintainable by removing unnecessary elements that
  add complexity without value:


  1. Remove unused header includes that increase compile times'
repository: vllm-project/vllm
label: Code Style
language: CUDA
comments_count: 5
repository_stars: 51730
---

Keep code clean and maintainable by removing unnecessary elements that add complexity without value:

1. Remove unused header includes that increase compile times
2. Delete commented-out code blocks - use version control to track alternatives
3. Eliminate redundant checks and validations
4. Clean up duplicate definitions

Example of code to avoid:
```cpp
#include <iostream>  // Unnecessary include

// Commented out alternative implementation
// void alternativeFunction() {
//   ...
// }

// Redundant checks
TORCH_CHECK(a_tensors.dtype() == torch::kFloat8_e4m3fn,
           "A tensors must be of type float8_e4m3fn.");
TORCH_CHECK(a_tensors.dtype() == torch::kFloat8_e4m3fn);  // Duplicate check
```

Instead, keep only the essential, active code elements and rely on version control for tracking alternatives.