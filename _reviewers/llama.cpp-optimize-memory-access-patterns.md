---
title: optimize memory access patterns
description: 'Ensure CUDA kernels use optimal memory access patterns to maximize performance.
  This involves several key practices:


  1. **Use `__restrict__` qualifiers** on pointer parameters to inform the compiler
  that pointers don''t alias, enabling better optimizations especially on older GPUs.'
repository: ggml-org/llama.cpp
label: Performance Optimization
language: CUDA
comments_count: 5
repository_stars: 83559
---

Ensure CUDA kernels use optimal memory access patterns to maximize performance. This involves several key practices:

1. **Use `__restrict__` qualifiers** on pointer parameters to inform the compiler that pointers don't alias, enabling better optimizations especially on older GPUs.

2. **Organize threads for coalesced memory access** by ensuring adjacent threads access adjacent memory locations. Map thread indices to tensor data as if the tensor was flattened, avoiding fractional warps.

3. **Use typed pointers instead of byte offsets** when possible, as explicit byte offset patterns perform poorly on GPUs compared to CPU code.

4. **Ensure proper thread-to-data mapping** to avoid uncoalesced accesses.

Example of proper thread organization for coalesced access:
```cuda
// Good: Adjacent threads access adjacent memory
const int i01 = blockIdx.x;
const int i00 = blockIdx.y*blockDim.x + threadIdx.x;

// Bad: Non-coalesced access pattern
const int i01 = blockDim.x * blockIdx.x + threadIdx.x;
const int i00 = blockIdx.y;
```

Example of using `__restrict__` qualifiers:
```cuda
static __global__ void kernel(
    const void * __restrict__ src0,
    void * __restrict__ dst,
    // ... other parameters
) {
    // kernel implementation
}
```

These optimizations are critical for GPU performance as memory bandwidth is often the limiting factor, and proper access patterns can significantly improve throughput.