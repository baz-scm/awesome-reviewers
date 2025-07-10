---
title: Use acks_late for reliability
description: Configure Celery tasks with `acks_late=True` when task reliability is
  critical and you prefer to risk duplicate processing rather than task loss. This
  setting ensures tasks aren't acknowledged until successfully completed, allowing
  them to be reprocessed if a worker crashes or a deployment occurs during task execution.
repository: getsentry/sentry
label: Celery
language: Python
comments_count: 2
repository_stars: 41297
---

Configure Celery tasks with `acks_late=True` when task reliability is critical and you prefer to risk duplicate processing rather than task loss. This setting ensures tasks aren't acknowledged until successfully completed, allowing them to be reprocessed if a worker crashes or a deployment occurs during task execution.

Without this setting, if a worker is killed during task processing (e.g., during a deployment), the task will be lost as it was already acknowledged when received by the worker.

Example:
```python
@instrumented_task(
    name="sentry.replays.tasks.run_bulk_replay_delete_job",
    queue="replays.delete_replay",
    acks_late=True,  # Ensure task durability during deployments
    default_retry_delay=5,
    max_retries=5,
    silo_mode=SiloMode.REGION,
    taskworker_config=TaskworkerConfig(namespace=replays_tasks, retry=Retry(times=5)),
)
def run_bulk_replay_delete_job(replay_delete_job_id: int, offset: int, limit: int = 100) -> None:
    # Task implementation...
```

This is especially important for chained tasks, long-running operations, or tasks working with critical data where task loss would be more problematic than potential duplicate processing.