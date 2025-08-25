---
title: Eliminate redundant operations
description: Avoid duplicate function calls, repeated tensor operations, and redundant
  computations that can significantly impact performance. Implement caching mechanisms
  for expensive operations and pre-allocate tensors when possible.
repository: sgl-project/sglang
label: Performance Optimization
language: Python
comments_count: 8
repository_stars: 17245
---

Avoid duplicate function calls, repeated tensor operations, and redundant computations that can significantly impact performance. Implement caching mechanisms for expensive operations and pre-allocate tensors when possible.

Key optimization strategies:
1. **Cache expensive function results**: Store results of costly operations like `get_normalized_target_modules()` or `is_npu()` to avoid repeated execution
2. **Pre-allocate tensors**: Use pre-allocated buffers instead of creating new tensors with `torch.arange()` or `torch.zeros()` in hot paths
3. **Avoid duplicate initialization**: Prevent initializing the same components multiple times (e.g., ragged wrappers) within a single forward pass
4. **Use lookup tables**: Pre-compute valid cases in lookup tables rather than dynamic computation when the search space is bounded

Example of caching expensive operations:
```python
# Before: Redundant calls
for lora_id, config in self.configs.items():
    user_normalized_modules = get_normalized_target_modules(config.target_modules)

# After: Cache and reuse
normalized_cache = {}
for lora_id, config in self.configs.items():
    if config.target_modules not in normalized_cache:
        normalized_cache[config.target_modules] = get_normalized_target_modules(config.target_modules)
    user_normalized_modules = normalized_cache[config.target_modules]
```

Example of pre-allocation:
```python
# Before: Creating tensors in hot path
q_indptr = torch.arange(0, bs + 1, dtype=torch.int32, device=device)

# After: Pre-allocate during initialization
self.q_indptr_decode = torch.arange(0, max_bs + 1, dtype=torch.int32, device=device)
# Use pre-allocated buffer: q_indptr = self.q_indptr_decode[:bs + 1]
```

Performance impact can be substantial - caching reduced execution time from 133μs to 5μs in one measured case. Always profile critical paths and eliminate redundant work through strategic caching and pre-allocation.