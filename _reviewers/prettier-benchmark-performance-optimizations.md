---
title: Benchmark performance optimizations
description: Always measure and validate performance optimizations with concrete benchmarks
  before implementing them. Performance assumptions can be misleading, and minor gains
  may not justify added complexity or reduced correctness.
repository: prettier/prettier
label: Performance Optimization
language: Markdown
comments_count: 2
repository_stars: 50772
---

Always measure and validate performance optimizations with concrete benchmarks before implementing them. Performance assumptions can be misleading, and minor gains may not justify added complexity or reduced correctness.

When considering performance optimizations:
1. Create reproducible benchmarks to measure actual impact
2. Test across different scenarios and project sizes
3. Consider whether the performance gain justifies any tradeoffs in correctness, maintainability, or user experience
4. Be willing to remove optimizations that don't provide meaningful benefits

Example from caching strategy evaluation:
```bash
# Benchmark showed minimal difference despite expectations
--cache-strategy=metadata x 0.30 ops/sec ±6.05% (5 runs sampled)
--cache-strategy=content x 0.30 ops/sec ±0.94% (5 runs sampled)

# Decision: Choose content strategy despite 10-20ms cost
# Reason: "For normal projects, there is no performance difference, 
# and content is more convenient"
```

Avoid premature optimization and be prepared to prioritize correctness and usability over marginal performance gains. If benchmarks show negligible differences, choose the option that provides better developer experience or system reliability.