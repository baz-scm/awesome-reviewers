---
title: Clear metric documentation
description: 'When adding, modifying, or deprecating metrics, ensure comprehensive
  and clear documentation. Include:


  1. Descriptive names for new metrics that reflect their purpose'
repository: vitessio/vitess
label: Observability
language: Markdown
comments_count: 2
repository_stars: 19815
---

When adding, modifying, or deprecating metrics, ensure comprehensive and clear documentation. Include:

1. Descriptive names for new metrics that reflect their purpose
2. Clear explanations of what each metric measures
3. The dimensions/labels available for the metric
4. Explicit mention of any deprecated metrics and their replacements

For example, when documenting a new metric:
```
### VTGate Metrics

Added two new metrics with query type, plan type and tablet type as dimensions:
1. QueryProcessed - This counts the number of queries processed
2. QueryRouted - This counts the number of shards the query was executed on

Deprecated:
1. QueriesProcessed - Replaced by QueryProcessed
2. TableMetrics - Replaced by QueryTables
```

This practice ensures users can effectively monitor their systems, understand metric changes, and maintain accurate dashboards and alerts as your observability tools evolve.