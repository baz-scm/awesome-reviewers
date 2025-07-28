---
title: prefer const variables
description: Add the `const` qualifier to variables that are not modified after initialization.
  This improves code clarity, prevents accidental modifications, and makes the code's
  intent more explicit to both compilers and other developers.
repository: ggml-org/llama.cpp
label: Code Style
language: CUDA
comments_count: 2
repository_stars: 83559
---

Add the `const` qualifier to variables that are not modified after initialization. This improves code clarity, prevents accidental modifications, and makes the code's intent more explicit to both compilers and other developers.

Apply `const` to:
- Local variables that are initialized once and never changed
- Function parameters that are not modified within the function
- Any variable where the value remains constant throughout its scope

Example transformations:
```cpp
// Before
float2 dsB;
dsB = __half22float2(y_dm[j*MMQ_TILE_Y_K + k01/QI8_1]);

int global_idx = blockIdx.x * blockDim.x + threadIdx.x;
int total_elements = batches * channels * out_h * out_w;

// After  
const float2 dsB = __half22float2(y_dm[j*MMQ_TILE_Y_K + k01/QI8_1]);

const int global_idx = blockIdx.x * blockDim.x + threadIdx.x;
const int total_elements = batches * channels * out_h * out_w;
```

This practice is especially important in CUDA kernels and performance-critical code where clarity about data mutability helps with optimization and debugging.