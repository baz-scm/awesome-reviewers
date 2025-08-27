---
title: Use benchmarked thresholds
description: Base performance-critical constants, limits, and thresholds on empirical
  benchmarking rather than arbitrary values. When implementing optimizations that
  involve numeric parameters—such as buffer size limits, inlining costs, or caching
  thresholds—conduct systematic benchmarking to determine optimal values and document
  the rationale.
repository: golang/go
label: Performance Optimization
language: Go
comments_count: 3
repository_stars: 129599
---

Base performance-critical constants, limits, and thresholds on empirical benchmarking rather than arbitrary values. When implementing optimizations that involve numeric parameters—such as buffer size limits, inlining costs, or caching thresholds—conduct systematic benchmarking to determine optimal values and document the rationale.

For memory management decisions, establish limits that balance performance gains with resource efficiency:

```go
func cacheEncodeState(e *encodeState) {
    // Threshold determined through benchmarking to balance 
    // memory efficiency vs. performance gains
    if e.Buffer.Cap() > 32768 {
        return // Don't cache large buffers
    }
    // ... cache the state
}

const (
    // 57 was benchmarked to provide most benefit with no bad surprises
    inlineExtraCallCost = 57
    // These values were benchmarked to provide most benefit
    inlineBigForCost = 105
)
```

When creating benchmarks, separate different scenarios to get granular performance data rather than combining multiple cases. This enables more precise optimization decisions and helps identify the specific conditions where performance improvements matter most.