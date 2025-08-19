---
title: leverage framework capabilities
description: Structure workflows and activities to take full advantage of the orchestration
  framework's built-in capabilities for fault tolerance, retries, and durable execution
  rather than implementing custom solutions.
repository: PostHog/posthog
label: Temporal
language: Python
comments_count: 2
repository_stars: 28460
---

Structure workflows and activities to take full advantage of the orchestration framework's built-in capabilities for fault tolerance, retries, and durable execution rather than implementing custom solutions.

Break down complex operations into separate, resumable steps that can leverage the framework's retry and restart mechanisms. Avoid duplicating functionality that the framework already provides automatically.

For example, instead of implementing a single monolithic operation that handles multiple steps internally:

```python
# Avoid: Single operation that can't resume individual steps
@dagster.op
def snapshot_all_project_data(context, project_id: int, s3: S3Resource):
    snapshot_postgres_data(...)  # If this succeeds but next fails,
    snapshot_clickhouse_data(...)  # we can't resume from here
    
# Prefer: Separate operations that can be retried independently  
@dagster.op
def snapshot_postgres_project_data(context, project_id: int, s3: S3Resource):
    # This can be retried/resumed independently
    
@dagster.op  
def snapshot_clickhouse_project_data(context, project_id: int, s3: S3Resource):
    # This can be retried/resumed independently
```

Similarly, remove redundant code when the framework already provides the needed functionality automatically, such as context attributes for metrics or built-in retry policies.