---
title: benchmark performance optimizations
description: Always measure and validate performance optimizations through benchmarking
  before assuming they provide benefits. Performance changes can have unexpected consequences,
  and what appears to be an optimization may actually degrade performance in real-world
  scenarios.
repository: facebook/yoga
label: Performance Optimization
language: JavaScript
comments_count: 2
repository_stars: 18255
---

Always measure and validate performance optimizations through benchmarking before assuming they provide benefits. Performance changes can have unexpected consequences, and what appears to be an optimization may actually degrade performance in real-world scenarios.

When implementing performance optimizations:
1. Create benchmarks that represent realistic usage patterns
2. Measure before and after performance metrics
3. Consider trade-offs between different performance aspects (memory vs computation, allocation vs GC pressure)
4. Document the measured improvements to justify the optimization

Example approach:
```javascript
// Before assuming this is faster:
return node.style[key] || node.style[type + key + suffix];

// Benchmark with realistic test cases:
// "in order to make sure that it has performance improvement, we need to benchmark it.
// Can you use the code that generates a random test to generate a big random tree 
// and then time the layout algorithm before and after? Otherwise we can't know 
// if this is a performance optimization or not."
```

This is especially important for layout algorithms and frequently-called code paths where performance assumptions can significantly impact application responsiveness.