---
title: Proper metrics design
description: 'When designing metrics for observability systems like Prometheus, follow
  established best practices to ensure your metrics are useful, queryable, and maintainable:'
repository: neondatabase/neon
label: Observability
language: Other
comments_count: 2
repository_stars: 19015
---

When designing metrics for observability systems like Prometheus, follow established best practices to ensure your metrics are useful, queryable, and maintainable:

1. Split metrics appropriately: Create separate metrics when aggregate operations (sum, avg) across dimensions wouldn't be meaningful. Don't combine unrelated measurements under a single metric name.

2. Use correct metric types: Select 'counter' for values that only increase (like event counts) and 'gauge' for values that can go up or down (like current status or measurements).

Example of proper metrics design:

```jsonnet
// GOOD: Separate metrics with clear meaning
{
  metric_name: 'pg_autovacuum_oldest_mxid',
  type: 'gauge',
  help: 'Oldest multi-transaction ID across all databases',
  key_labels: ['database_name'],
},
{
  metric_name: 'pg_autovacuum_oldest_frozen_xid',
  type: 'gauge',
  help: 'Oldest frozen transaction ID across all databases',
  key_labels: ['database_name'],
},
{
  metric_name: 'pg_autovacuum_run_count',
  type: 'counter',  // Counter for non-decreasing values
  help: 'Number of autovacuum runs',
  key_labels: ['database_name', 'table_name'],
}

// BAD: Combined unrelated metrics with unclear aggregation meaning
{
  metric_name: 'pg_autovacuum_stats',
  type: 'gauge',  // Wrong type for counts
  help: 'Autovacuum statistics for all tables across databases',
  key_labels: ['database_name'],
  value_label: 'metric',
  values: ['oldest_mxid', 'oldest_frozen_xid', 'run_count'],
}
```

Reference: https://prometheus.io/docs/practices/naming/