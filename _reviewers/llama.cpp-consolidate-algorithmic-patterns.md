---
title: consolidate algorithmic patterns
description: Avoid duplicating similar algorithmic logic across multiple functions
  by consolidating them into generic, templated, or trait-based implementations. This
  reduces maintenance burden and improves code consistency.
repository: ggml-org/llama.cpp
label: Algorithms
language: CUDA
comments_count: 11
repository_stars: 83559
---

Avoid duplicating similar algorithmic logic across multiple functions by consolidating them into generic, templated, or trait-based implementations. This reduces maintenance burden and improves code consistency.

Instead of creating separate functions for each data type or operation combination, use templates or generic approaches:

```cpp
// Avoid this - separate functions for each type combination
static __device__ void convert_f32_f32(const float * src, float * dst) { *dst = *src; }
static __device__ void convert_f16_f32(const half * src, float * dst) { *dst = *src; }
static __device__ void convert_bf16_f32(const nv_bfloat16 * src, float * dst) { *dst = *src; }

// Prefer this - generic template approach
template<typename src_t, typename dst_t>
static __device__ __forceinline__ void convert_to_flt(const src_t * src, dst_t * dst) {
    *dst = float(*src);  // Convert through float as common intermediate
}
```

Similarly, for algorithmic logic that varies only by parameters, use templates instead of switch statements or multiple similar functions:

```cpp
// Instead of separate functions for each granularity calculation
static int mmq_get_granularity_host(ggml_type type, const int mmq_x, const int cc) {
    // Use trait-based approach or template specialization
}

// Consider using trait structs for type-specific behavior
template<ggml_type T> struct mmq_type_traits {
    static constexpr int granularity(int mmq_x) { /* type-specific logic */ }
};
```

This approach is particularly important for computational kernels where similar patterns appear across different data types or operation sizes. Look for opportunities to extract common algorithmic patterns into reusable, parameterized implementations.