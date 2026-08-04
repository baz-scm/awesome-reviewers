---
title: Validated Observability Guidance
description: 'When updating observability docs, dashboards, or diagnostic query packs,
  ensure the guidance is both actionable and correct:


  1) Add critical alerting/scale guidance'
repository: awslabs/mcp
label: Observability
language: Markdown
comments_count: 2
repository_stars: 9545
---

When updating observability docs, dashboards, or diagnostic query packs, ensure the guidance is both actionable and correct:

1) Add critical alerting/scale guidance
- For “critical outage” gotchas, include what to monitor (e.g., resource utilization), recommended thresholds, and the alarm purpose (e.g., “scale compute if needed”). Link to the relevant monitoring/config optimization docs.

2) Prevent metric misinterpretation
- Explicitly state when a signal is ambiguous and what metric(s) confirm the real condition.
- Example principle: don’t equate “increased waits for X” with the underlying conflict/storm; validate with the dedicated conflict metrics.

3) Publish reusable, parameterized query snippets
- Provide templated queries (replace CLUSTER_ID / label values), and include time-range + step guidance for range queries.

Example (patterned PromQL + interpretation note):
```promql
# Template: replace CLUSTER_ID
execute_promql_query(
  query='sum(db.active_sessions.avg{@resource.aws.auroradsql.cluster_id="CLUSTER_ID"})'
)

# Range query with documented steps
execute_promql_range_query(
  query='sum by (wait_event)(db.active_sessions.avg{@resource.aws.auroradsql.cluster_id="CLUSTER_ID"})',
  start="START_TIME", end="END_TIME", step="300s"
)

# Interpretation note:
# If commit waits rise, confirm conflict storms using the dedicated conflict indicators
# (e.g., TotalTransactions/OccConflicts), since commit waits alone can mean many sessions are just committing.
```

This standard reduces outage risk by pairing alerts with “what to do next,” and improves diagnostic reliability by encoding correct metric semantics and validated query patterns.