---
title: Optimize metrics label cardinality
description: 'Carefully manage metric label cardinality to prevent excessive memory
  usage and maintain system performance. Follow these guidelines:


  1. Separate high-cardinality metrics:'
repository: temporalio/temporal
label: Observability
language: Go
comments_count: 5
repository_stars: 14953
---

Carefully manage metric label cardinality to prevent excessive memory usage and maintain system performance. Follow these guidelines:

1. Separate high-cardinality metrics:
   - Use counters without labels for high-cardinality dimensions (e.g., namespace)
   - Reserve latency metrics for low-cardinality labels only

2. Use dedicated metrics for different granularities:
   - Create separate metrics for namespace-level tracking
   - Use interceptors for consistent label application

Example:
```go
// DON'T: High cardinality labels on latency metrics
metrics.OperationLatency.With(metricsHandler).
    WithTags(metrics.NamespaceTag(namespace)).Record(elapsed)

// DO: Separate counter for namespace-level tracking
metricsHandler = metricsHandler.WithTags(metrics.TargetClusterTag(clusterName))
if len(namespaceName) != 0 {
    // Add namespace tag only to counter metrics
    metricsHandler = metricsHandler.WithTags(metrics.NamespaceTag(namespaceName))
}
metrics.OperationCount.With(metricsHandler).Record(1)
```

3. For error tracking:
   - Use separate error counters with appropriate labels
   - Consider the cardinality impact when adding error type labels