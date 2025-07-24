---
title: special value handling
description: Algorithms must explicitly define and consistently handle special values
  like NaN, infinity, and edge cases across all mathematical operations. Special values
  can significantly impact computational results and should not be treated as afterthoughts.
repository: prometheus/prometheus
label: Algorithms
language: Markdown
comments_count: 4
repository_stars: 59616
---

Algorithms must explicitly define and consistently handle special values like NaN, infinity, and edge cases across all mathematical operations. Special values can significantly impact computational results and should not be treated as afterthoughts.

Key requirements:
- Document how NaN values are handled in each algorithm (e.g., "NaN is considered the smallest possible value" for quantile operations)
- Specify behavior when special values are encountered (e.g., "NaN observations are considered outside of any buckets")
- Ensure IEEE 754 floating point arithmetic compliance where applicable
- Handle mixed data types appropriately (float vs histogram samples)

Example from PromQL aggregation functions:
```
// Good: Explicit NaN handling documentation
`quantile(phi, v)` calculates the φ-quantile, with NaN considered 
the smallest possible value for ranking purposes.

// Good: Special case documentation  
Special case for native histograms: NaN observations are considered 
outside of any buckets. `histogram_fraction(-Inf, +Inf, b)` may 
therefore be less than 1.
```

This prevents unexpected behavior and ensures algorithmic correctness, especially in statistical and mathematical computations where special values have well-defined meanings.