---
title: Optimize numerical precision
description: When implementing AI operations that involve matrix multiplication or
  neural network components, explicitly support modern numerical precision formats
  (TF32, BFloat16, Float8) across different hardware backends. These precision formats
  significantly accelerate AI training and inference while maintaining acceptable
  numerical accuracy.
repository: pytorch/pytorch
label: AI
language: C++
comments_count: 8
repository_stars: 91345
---

When implementing AI operations that involve matrix multiplication or neural network components, explicitly support modern numerical precision formats (TF32, BFloat16, Float8) across different hardware backends. These precision formats significantly accelerate AI training and inference while maintaining acceptable numerical accuracy.

For maximum performance:
1. Ensure consistent precision format support across hardware accelerators (CUDA, XPU, MKL-DNN)
2. Handle different accelerator types with appropriate conditionals:
```cpp
if ((input_.is_cuda() || input_.is_xpu()) && input_.scalar_type() == ScalarType::Half) {
  // Use accelerator-specific optimizations
}
```
3. Implement specialized code paths for each precision format (ieee, tf32, bf16) based on the operation requirements
4. Add unit tests to verify numerical correctness when using reduced-precision formats

These optimizations can lead to significant speedups in large model training and inference without requiring algorithm changes.