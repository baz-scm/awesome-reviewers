---
title: Concurrent resource management
description: When implementing concurrent operations, properly manage shared resources
  to prevent race conditions and ensure system stability. Use database-level locking
  mechanisms like `SELECT ... FOR UPDATE SKIP LOCKED` to prevent concurrent access
  to the same data. Configure thread pools with appropriate limits and timeouts to
  avoid resource exhaustion. Separate...
repository: langgenius/dify
label: Concurrency
language: Python
comments_count: 6
repository_stars: 114231
---

When implementing concurrent operations, properly manage shared resources to prevent race conditions and ensure system stability. Use database-level locking mechanisms like `SELECT ... FOR UPDATE SKIP LOCKED` to prevent concurrent access to the same data. Configure thread pools with appropriate limits and timeouts to avoid resource exhaustion. Separate different types of tasks into distinct queues to prevent blocking.

Key practices:
- Use database locks for concurrent data access: `query.with_for_update(skip_locked=True)`
- Set explicit worker limits: `ThreadPoolExecutor(max_workers=1)` when sequential processing is required
- Add timeouts to concurrent operations: `concurrent.futures.wait(futures, timeout=30)`
- Implement time-windowing for high-frequency updates to reduce contention
- Separate task types into different queues: `@shared_task(queue="schedule")` vs `@shared_task(queue="execution")`

Example of proper concurrent resource management:
```python
# Use database locking to prevent race conditions
with session_factory() as session:
    schedules = session.scalars(
        query.with_for_update(skip_locked=True).limit(batch_size)
    )
    
# Configure thread pools with appropriate limits and timeouts
with ThreadPoolExecutor(max_workers=3) as executor:
    futures = [executor.submit(process_item, item) for item in items]
    concurrent.futures.wait(futures, timeout=30)
```

Document thread safety requirements for shared components and avoid synchronous blocking patterns in async systems.