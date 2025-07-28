---
title: Metal shared memory sizing
description: When allocating shared memory for Metal compute shaders, ensure proper
  sizing that accounts for both SIMD group requirements and Metal platform constraints.
  Metal requires shared memory buffer sizes to be multiples of 16 bytes. Consider
  using simplified allocation strategies that meet platform requirements while maintaining
  correctness.
repository: ggml-org/llama.cpp
label: Performance Optimization
language: Objective-C
comments_count: 2
repository_stars: 83559
---

When allocating shared memory for Metal compute shaders, ensure proper sizing that accounts for both SIMD group requirements and Metal platform constraints. Metal requires shared memory buffer sizes to be multiples of 16 bytes. Consider using simplified allocation strategies that meet platform requirements while maintaining correctness.

For SIMD-based operations, you can often allocate a fixed amount of shared memory for simplicity rather than complex calculations:

```objc
// Simple approach - ensures Metal alignment requirements
const int64_t shmem_size = 32; // 32*sizeof(float) bytes
[encoder setThreadgroupMemoryLength:shmem_size*sizeof(float) atIndex:0];
```

This approach handles Metal's alignment requirements automatically while providing sufficient memory for typical SIMD operations. When precise sizing is needed, ensure the calculated size accounts for the number of SIMD groups in the threadgroup (typically `d_state / simd_size`) but always verify the result meets Metal's 16-byte alignment constraint.