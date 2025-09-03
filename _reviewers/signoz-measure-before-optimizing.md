---
title: measure before optimizing
description: Always measure performance impact before making optimization decisions
  or skipping potential optimizations due to complexity assumptions. Performance characteristics
  can be counterintuitive, and assumptions about complexity vs. performance trade-offs
  should be validated with actual benchmarks.
repository: SigNoz/signoz
label: Performance Optimization
language: Go
comments_count: 3
repository_stars: 23369
---

Always measure performance impact before making optimization decisions or skipping potential optimizations due to complexity assumptions. Performance characteristics can be counterintuitive, and assumptions about complexity vs. performance trade-offs should be validated with actual benchmarks.

Key practices:
- Test performance impact of optimizations before dismissing them as "too complex"
- Compare different algorithmic approaches with benchmarks (e.g., regex vs direct lookups)
- Measure memory usage vs database roundtrip trade-offs in caching strategies
- Use profiling data to guide optimization priorities

Example from the codebase: Resource filters were initially skipped in trace operators due to complexity concerns, but after performance testing showed benefits, they were implemented. Similarly, regex matching was replaced with direct lookups after discovering it was 5x slower.

This approach prevents premature optimization while ensuring that beneficial optimizations aren't overlooked due to unfounded complexity concerns.