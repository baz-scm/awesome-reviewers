---
title: Validate configuration changes
description: Before modifying default configuration settings, thoroughly understand
  and test their implications. Django's default configurations often include important
  safeguards that prevent subtle bugs.
repository: django/django
label: Configurations
language: Txt
comments_count: 3
repository_stars: 84182
---

Before modifying default configuration settings, thoroughly understand and test their implications. Django's default configurations often include important safeguards that prevent subtle bugs.

For example, the `ENQUEUE_ON_COMMIT` setting in task backends defaults to `True` for good reason:

```python
@task
def my_task():
    Thing.objects.get(id=thing_id)  # Could fail if transaction hasn't committed yet

with transaction.atomic():
    thing = Thing.objects.create()
    my_task.enqueue(thing_id=thing.id)
    # With ENQUEUE_ON_COMMIT=False, task might run before transaction commits
```

Similarly, the `QUEUES` restriction in task backends prevents typos that could cause tasks to be enqueued but never executed.

When working with time-sensitive data, be particularly careful with timezone configurations as they can lead to unexpected query results when using functions like `Trunc` across different environments.

Always test configuration changes across all target environments before deployment, as some issues only manifest in specific contexts or at scale.