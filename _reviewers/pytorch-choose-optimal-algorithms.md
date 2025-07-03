---
title: Choose optimal algorithms
description: Select algorithms and data structures that optimize for computational
  efficiency based on the specific problem requirements. When working with matrices
  or multi-dimensional data, ensure index calculations correctly map to the underlying
  memory layout. Use compile-time optimizations like `if constexpr` over runtime conditionals
  when the condition is known at...
repository: pytorch/pytorch
label: Algorithms
language: Other
comments_count: 10
repository_stars: 91169
---

Select algorithms and data structures that optimize for computational efficiency based on the specific problem requirements. When working with matrices or multi-dimensional data, ensure index calculations correctly map to the underlying memory layout. Use compile-time optimizations like `if constexpr` over runtime conditionals when the condition is known at compile time.

For example, instead of:
```cpp
if (!rms_norm) {
  wd = cuWelfordOnlineSum(static_cast<acc_t>(data.val[ii]), wd);
} else {
  wd = cuRMSOnlineSum(static_cast<acc_t>(data.val[ii]), wd);
}
```

Prefer:
```cpp
if constexpr (!rms_norm) {
  wd = cuWelfordOnlineSum(static_cast<acc_t>(data.val[ii]), wd);
} else {
  wd = cuRMSOnlineSum(static_cast<acc_t>(data.val[ii]), wd);
}
```

For iterators and algorithms, prefer standard library implementations over custom ones when available. In CUDA code, use thrust iterators like `thrust::transform_iterator` and `thrust::make_transform_iterator` instead of custom iterator implementations:

```cpp
// Instead of:
auto iter = NO_ROCM(at_cuda_detail)::cub::TransformInputIterator<bool, NonZeroOp<scalar_t>, const scalar_t*>(
    self_.const_data_ptr<scalar_t>() + idx * chunk_size, NonZeroOp<scalar_t>());

// Prefer:
auto iter = thrust::make_transform_iterator(
    self_.const_data_ptr<scalar_t>() + idx * chunk_size, NonZeroOp<scalar_t>());
```

When implementing sorting or comparison operations, be aware of how the standard library compares objects like `std::pair` (lexicographically by default) and document any custom comparators when non-standard behavior is needed.
