---
title: Benchmark performance changes
description: Always measure and validate performance impact through benchmarking before
  making changes that could affect system performance, even when changes appear to
  be obvious optimizations. Removing seemingly redundant configurations or adding
  new features can have unexpected performance consequences that only surface during
  integration testing or production use.
repository: kubernetes/kubernetes
label: Performance Optimization
language: Yaml
comments_count: 2
repository_stars: 116489
---

Always measure and validate performance impact through benchmarking before making changes that could affect system performance, even when changes appear to be obvious optimizations. Removing seemingly redundant configurations or adding new features can have unexpected performance consequences that only surface during integration testing or production use.

Before making performance-related changes:
1. Establish baseline performance metrics
2. Create performance test variants to compare before/after scenarios  
3. Run comprehensive benchmarks across relevant scenarios
4. Validate that changes don't break existing performance requirements

Example from resource configuration:
```yaml
resources:
  requests:
    foo.com/bar-{{.Index}}: 1
  limits:
    foo.com/bar-{{.Index}}: 1  # Don't remove without testing - may be required for non-overcommitable resources
```

Performance validation should include both automated benchmarks and integration tests to catch issues like "Limit must be set for non overcommitable resources" that only appear in specific runtime conditions. Document performance comparison results with statistical significance testing to make informed decisions about optimization trade-offs.