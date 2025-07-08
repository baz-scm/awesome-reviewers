---
title: Task signature methods
description: 'When chaining Celery tasks, choose the correct signature method:

  - Use `.s()` when a task needs the output from the previous task in the chain

  - Use `.si()` (immutable signature) when a task doesn''t need any output from the
  previous task'
repository: prowler-cloud/prowler
label: Celery
language: Python
comments_count: 2
repository_stars: 11834
---

When chaining Celery tasks, choose the correct signature method:
- Use `.s()` when a task needs the output from the previous task in the chain
- Use `.si()` (immutable signature) when a task doesn't need any output from the previous task

Incorrect signature methods can cause task failures or unexpected data flow between tasks.

```python
# Example of proper signature method usage:
chain(
    initial_task.si(param1=value1),  # First task or doesn't need previous output
    process_results.s(),  # Needs output from initial_task
    save_to_database.si(param2=value2)  # Independent task with static parameters
)
```