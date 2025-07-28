---
title: prioritize compile-time optimizations
description: 'In performance-critical code, favor compile-time optimizations over
  runtime flexibility to enable better compiler optimizations and reduce execution
  overhead. This principle applies to several key areas:'
repository: ggml-org/llama.cpp
label: Performance Optimization
language: Other
comments_count: 4
repository_stars: 83559
---

In performance-critical code, favor compile-time optimizations over runtime flexibility to enable better compiler optimizations and reduce execution overhead. This principle applies to several key areas:

**Use compile-time constants instead of runtime values:** Replace runtime function calls with compile-time constants when the values are known at compile time. For example, use `#define WG_M 16` instead of `get_local_size()` in GPU kernels, as compile-time constants allow the compiler to fully unroll loops and pre-calculate memory address offsets.

**Enable loop unrolling with compiler hints:** Add `[[unroll]]` annotations to loops with constant trip counts, especially in nested loop scenarios where the compiler might not automatically unroll:

```cpp
[[unroll]] for (uint j = 0; j < NUM_COLS; ++j) {
    [[unroll]] for (uint n = 0; n < num_rows; ++n) {
        temp[j][n] = subgroupClusteredAdd(temp[j][n], GROUP_SIZE);
    }
}
```

**Eliminate branches through constant folding:** Structure code so the compiler can inline functions and fold constants, rather than using runtime boolean expressions in hot loops. Write separate functions for different code paths and let the compiler optimize each path independently.

**Prefer build-time compilation:** When possible, compile shaders and other performance-critical code at build time rather than runtime to avoid compilation overhead and enable better optimization opportunities.

These techniques are particularly important in GPU kernels, SIMD code, and other performance-critical paths where even small optimizations can yield significant performance improvements (10-17% gains are common).