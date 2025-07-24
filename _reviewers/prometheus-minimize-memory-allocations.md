---
title: minimize memory allocations
description: Prioritize memory allocation minimization through buffer reuse, pre-allocation,
  and efficient data structures. Allocations are among the worst performance bottlenecks,
  especially in hot paths and frequently called functions.
repository: prometheus/prometheus
label: Performance Optimization
language: Go
comments_count: 9
repository_stars: 59616
---

Prioritize memory allocation minimization through buffer reuse, pre-allocation, and efficient data structures. Allocations are among the worst performance bottlenecks, especially in hot paths and frequently called functions.

Key strategies:
1. **Reuse buffers and slices**: Instead of creating new slices, resize existing ones to zero length and reuse capacity
2. **Pre-allocate with known sizes**: Use `make([]T, len)` instead of `make([]T, 0, len)` with `append()` when the final size is known
3. **Use memory pools judiciously**: Return objects to pools before populating new ones, but avoid pools for large, infrequently used objects
4. **Choose efficient data structures**: Use `struct{}` instead of `bool` for existence-only maps, and prefer smaller integer types when ranges allow

Example of buffer reuse:
```go
// Instead of creating new slices
to.NegativeSpans = nil
to.NegativeBuckets = nil

// Reuse existing capacity
if to.NegativeSpans != nil {
    to.NegativeSpans = to.NegativeSpans[:0]
}
if to.NegativeBuckets != nil {
    to.NegativeBuckets = to.NegativeBuckets[:0]
}
```

Example of pre-allocation:
```go
// Instead of append() with unknown final size
vs.Series = make([]storage.Series, 0, len(mat))
for _, s := range mat {
    vs.Series = append(vs.Series, NewStorageSeries(s))
}

// Pre-allocate and index directly
vs.Series = make([]storage.Series, len(mat))
for i, s := range mat {
    vs.Series[i] = NewStorageSeries(s)
}
```

Always profile allocation-heavy code paths and consider the memory lifecycle of objects, especially in high-frequency operations like query evaluation, scraping, and data ingestion.