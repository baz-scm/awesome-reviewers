---
title: optimize tensor operations
description: When working with PyTorch tensors, prioritize operations that avoid unnecessary
  memory allocations and copies to improve performance. Choose tensor operations carefully
  based on whether data will be immediately overwritten or needs preservation.
repository: sgl-project/sglang
label: Pytorch
language: Python
comments_count: 3
repository_stars: 17245
---

When working with PyTorch tensors, prioritize operations that avoid unnecessary memory allocations and copies to improve performance. Choose tensor operations carefully based on whether data will be immediately overwritten or needs preservation.

Key guidelines:
- Use `tensor.view(dtype)` instead of `tensor.to(dtype)` when possible to avoid copies
- Use `torch.empty()` instead of `torch.zeros()` when the tensor will be fully populated immediately after creation
- Understand memory allocation contexts (like symmetric memory pools) and their implications for tensor operations

Example:
```python
# Avoid unnecessary copy
if tensor.dtype != target_dtype:
    tensor = tensor.view(target_dtype)  # No copy if compatible
    # instead of: tensor = tensor.to(target_dtype)  # May cause copy

# Avoid unnecessary initialization
kv_indices = torch.empty(size, dtype=torch.int32)  # Will be filled next
# instead of: kv_indices = torch.zeros(size, dtype=torch.int32)  # Extra kernel launch
```

This approach reduces memory overhead and kernel launches, leading to better performance in tensor-heavy operations.