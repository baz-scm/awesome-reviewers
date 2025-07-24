---
title: simplify complex algorithms
description: When implementing algorithms, prioritize simplicity and maintainability
  over premature optimization. Complex algorithms should be broken down into smaller,
  reusable components or replaced with simpler approaches when possible.
repository: prometheus/prometheus
label: Algorithms
language: Go
comments_count: 10
repository_stars: 59616
---

When implementing algorithms, prioritize simplicity and maintainability over premature optimization. Complex algorithms should be broken down into smaller, reusable components or replaced with simpler approaches when possible.

Key principles:
- Choose the simplest algorithm that meets requirements first, then optimize if needed
- Break complex algorithms into smaller, testable functions with clear responsibilities  
- Consider computational complexity tradeoffs - sometimes a slightly less optimal but much simpler approach is better
- Avoid nested complexity layers that make code hard to understand and debug
- Use well-established algorithms and data structures rather than custom complex solutions

For example, instead of implementing complex bucket-level histogram manipulation:

```go
// Complex approach - manipulating individual buckets
for bucketIndex, bucketVal := range resultHistogram.PositiveBuckets {
    if bucketVal <= 0 {
        continue
    }
    bucketStartVal := firstH.PositiveBuckets[bucketIndex]
    bucketDelta := bucketVal * deltaScale
    predictedAtStart := bucketStartVal - (bucketDelta / sampledInterval * durationToStart)
    // ... more complex logic
}
```

Prefer a simpler count-based approach:

```go
// Simpler approach - use overall count for decisions
durationToZero := sampledInterval * (samples.Histograms[0].H.Count / resultHistogram.Count)
if durationToZero < durationToStart {
    durationToStart = durationToZero
}
```

This approach reduces complexity, improves maintainability, and often performs better while being easier to reason about and test.