---
title: Optimize tensor memory operations
description: When working with PyTorch tensors, use memory-efficient operations that
  avoid unnecessary copies. Specify memory formats directly during tensor creation
  instead of applying operations like `.t().contiguous()`. For C++/CUDA kernel interfacing,
  use `.data_ptr()` instead of `.view(dtype)` to ensure safe memory access and maintain
  compatibility with future...
repository: vllm-project/vllm
label: Pytorch
language: Python
comments_count: 2
repository_stars: 51730
---

When working with PyTorch tensors, use memory-efficient operations that avoid unnecessary copies. Specify memory formats directly during tensor creation instead of applying operations like `.t().contiguous()`. For C++/CUDA kernel interfacing, use `.data_ptr()` instead of `.view(dtype)` to ensure safe memory access and maintain compatibility with future PyTorch versions.

```python
# Inefficient approach with unnecessary copy:
tensor = torch.empty((n, m), device="cuda", dtype=torch.bfloat16).t().contiguous()

# Efficient approach:
tensor = torch.empty((n, m), device="cuda", dtype=torch.bfloat16, 
                     memory_format=torch.contiguous_format).t()

# Unsafe C++ kernel interfacing:
cutlass_function(w1_scale.view(torch.int32), w1.view(torch.long))

# Safe approach with explicit pointer access:
cutlass_function(w1_scale.data_ptr(), w1.data_ptr())
```