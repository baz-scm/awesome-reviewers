---
title: Metric design best practices
description: 'Design metrics to be reliable and maintainable by following these key
  principles:


  1. Initialize metrics with zero values to ensure consistent existence:'
repository: vitessio/vitess
label: Observability
language: Go
comments_count: 4
repository_stars: 19815
---

Design metrics to be reliable and maintainable by following these key principles:

1. Initialize metrics with zero values to ensure consistent existence:
```go
labelValues := []string{keyspace, shard, tabletType}
metrics.vstreamsEndedWithErrors.Add(labelValues, 0)
```

2. Choose appropriate metric granularity:
- Consider per-component metrics when aggregation could mask issues
- For streaming/processing, track per-shard metrics to identify bottlenecks
- Avoid overly granular labels (e.g., hostnames) that can explode cardinality

3. Select stable label dimensions:
- Use static identifiers (keyspace, shard, type)
- Avoid ephemeral values like hostnames in container environments
- Consider the metric lifespan and deployment environment

4. Handle metric lifecycle properly:
- Avoid metric re-registration issues
- Implement proper cleanup for deprecated metrics
- Document metric deprecation with clear replacement paths

These practices ensure metrics remain useful for debugging production issues while staying maintainable over time.