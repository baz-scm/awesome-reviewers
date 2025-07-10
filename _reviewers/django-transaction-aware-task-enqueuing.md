---
title: Transaction-aware task enqueuing
description: When working with background tasks that depend on database changes, ensure
  tasks are enqueued only after the related transaction has successfully committed.
  This prevents tasks from operating on uncommitted or rolled-back data, avoiding
  race conditions and inconsistent states.
repository: django/django
label: Celery
language: Txt
comments_count: 3
repository_stars: 84182
---

When working with background tasks that depend on database changes, ensure tasks are enqueued only after the related transaction has successfully committed. This prevents tasks from operating on uncommitted or rolled-back data, avoiding race conditions and inconsistent states.

The `ENQUEUE_ON_COMMIT` setting (defaulting to `True`) is crucial when using database-backed task queues as it enables atomic operations where both application data and tasks are committed together:

```python
from django.tasks import task
from django.db import transaction

@task()  # Uses default enqueue_on_commit=True
def process_order(order_id):
    # This task will only run after the transaction commits
    # ensuring the order exists in the database
    ...

# In your view or service:
with transaction.atomic():
    order = Order.objects.create(...)
    # The task will be enqueued when the transaction commits
    process_order.enqueue(order.id)
```

When testing or developing, you might choose different backends with appropriate transaction behavior, but always be mindful of how transaction handling will differ in production. Consider organizing tasks in a dedicated `tasks.py` module within each app to maintain consistent task discovery patterns.