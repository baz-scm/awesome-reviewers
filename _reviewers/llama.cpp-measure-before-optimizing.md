---
title: measure before optimizing
description: Always profile and measure performance impact before implementing optimizations,
  especially micro-optimizations. Many seemingly beneficial optimizations provide
  no measurable improvement and can hurt code maintainability.
repository: ggml-org/llama.cpp
label: Performance Optimization
language: C++
comments_count: 5
repository_stars: 83559
---

Always profile and measure performance impact before implementing optimizations, especially micro-optimizations. Many seemingly beneficial optimizations provide no measurable improvement and can hurt code maintainability.

Before adding performance optimizations:
1. Use proper profiling tools to identify actual bottlenecks
2. Measure the current performance with realistic workloads  
3. Implement the optimization
4. Measure again to verify the improvement is significant
5. Consider the maintenance cost vs. performance gain

Example from optimizer parameter pre-computation:
```cpp
// Before: Micro-optimization attempt
const float keep = 1.0f - opt_pars.adamw.alpha * opt_pars.adamw.wd;

// After measurement: "the micro-optimization has no visible benefit in this case"
// Reverted to simpler, more maintainable code
```

Common scenarios where measurement reveals optimizations are ineffective:
- CPU-bound optimizations in I/O-bound operations
- Micro-optimizations in infrequently called code paths  
- Complex optimizations with "microscopic" performance gains
- Operations that run once per request rather than per iteration

Use profiling-enabled tools when available (e.g., `enqueue_nd_range` for kernel timing) and prefer `steady_clock` over `high_resolution_clock` for accurate timing measurements. Remember that maintainability and code clarity often outweigh minimal performance gains.