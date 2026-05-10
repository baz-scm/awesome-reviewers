---
title: Synchronized Async Handoffs
description: 'When delegating work to concurrent/asynchronous execution (tasks, workers,
  background processes), ensure:

  1) **State ordering:** the async code cannot observe missing/partial state. For
  DB-backed workflows, enqueue/start tasks only after the transaction commits.'
repository: celery/celery
label: Concurrency
language: Other
comments_count: 2
repository_stars: 28464
---

When delegating work to concurrent/asynchronous execution (tasks, workers, background processes), ensure:
1) **State ordering:** the async code cannot observe missing/partial state. For DB-backed workflows, enqueue/start tasks only after the transaction commits.
2) **Lifecycle safety:** concurrent worker processes must be cleaned up when the parent/master process exits so you don’t leave orphaned workers running.

Example (transaction commit before enqueue):
```python
from django.db import transaction

def create_article_and_process(request):
    article = Article(...)  # fill fields

    with transaction.atomic():
        article.save()

        def enqueue_task():
            process_article.delay(article.pk)

        transaction.on_commit(enqueue_task)

    return response_ok()
```

Checklist:
- If a background task depends on data written in the current transaction, use a commit hook (e.g., `transaction.on_commit`) or equivalent “after commit” mechanism.
- For prefork/worker pools or any process-based concurrency, confirm orphaned worker processes are automatically terminated when the main process exits (or add explicit supervision/termination).