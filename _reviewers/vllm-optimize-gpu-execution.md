---
title: Optimize GPU execution
description: 'Ensure GPU code is optimized for both proper thread utilization and
  correct architecture dispatching:


  1. **Maximize thread parallelism** - Design CUDA kernels to fully utilize available
  threads. When appropriate, use multi-dimensional grid configurations to parallelize
  across all relevant dimensions of your problem.'
repository: vllm-project/vllm
label: Performance Optimization
language: CUDA
comments_count: 2
repository_stars: 51730
---

Ensure GPU code is optimized for both proper thread utilization and correct architecture dispatching:

1. **Maximize thread parallelism** - Design CUDA kernels to fully utilize available threads. When appropriate, use multi-dimensional grid configurations to parallelize across all relevant dimensions of your problem.

```cuda
// Instead of TODO comments like:
// TODO utilize more CUDA threads
// this will probably need some extra padding for warps

// Consider implementing a 2D grid approach:
dim3 block_dim(32, 8);  // Thread block dimensions
dim3 grid_dim((n + block_dim.x - 1) / block_dim.x, 
             (padded_m + block_dim.y - 1) / block_dim.y);
kernel<<<grid_dim, block_dim>>>(...);
```

2. **Implement proper architecture dispatching** - When supporting multiple GPU architectures, combine compile-time preprocessor directives with runtime architecture detection:

```cuda
// Instead of compile-time only checks:
#if defined ENABLE_CUTLASS_MOE_SM100 && ENABLE_CUTLASS_MOE_SM100
  if (version_num >= 100) {  // Use runtime version check
    cutlass_moe_mm_sm100(out_tensors, a_tensors, b_tensors, a_scales, b_scales,
                       expert_offsets, problem_sizes, a_strides, b_strides,
                       c_strides, per_act_token, per_out_ch);
    return;
  }
#endif
```

These approaches prevent performance bottlenecks and ensure code works correctly across different GPU hardware generations.