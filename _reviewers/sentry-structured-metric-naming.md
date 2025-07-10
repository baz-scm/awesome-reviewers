---
title: Structured metric naming
description: Create metrics with descriptive, unique names that are distinguishable
  when viewed in monitoring tools. Avoid generic prefixes that make groups of related
  metrics indistinguishable from each other. Include specific actions or states in
  the metric name to clearly identify what's being measured.
repository: getsentry/sentry
label: Observability
language: Python
comments_count: 3
repository_stars: 41297
---

Create metrics with descriptive, unique names that are distinguishable when viewed in monitoring tools. Avoid generic prefixes that make groups of related metrics indistinguishable from each other. Include specific actions or states in the metric name to clearly identify what's being measured.

For example, instead of:
```python
metrics.incr(
    "group.update.http_response",
    # This uses the same prefix as other methods, making metrics indistinguishable
)
```

Use:
```python
metrics.incr(
    "group.details.http_response",  # More specific to this particular operation
    tags={"method": "GET"},  # Add relevant dimensions for filtering
)
```

Additionally, place metrics as close as possible to the code they're measuring to maintain clear correlations between code execution and performance data. Consider creating helper functions that provide consistent metric naming within a module or service.

When adding context to metrics via tags, be mindful of cardinality concerns - limit high-cardinality tags (like user IDs) to avoid performance issues with your monitoring system.