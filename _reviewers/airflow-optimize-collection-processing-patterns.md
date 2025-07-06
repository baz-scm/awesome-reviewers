---
title: Optimize collection processing patterns
description: Use Python's built-in efficient collection processing methods instead
  of manual implementations. This reduces code complexity and improves performance
  by leveraging optimized implementations.
repository: apache/airflow
label: Algorithms
language: Python
comments_count: 4
repository_stars: 40858
---

Use Python's built-in efficient collection processing methods instead of manual implementations. This reduces code complexity and improves performance by leveraging optimized implementations.

Key practices:
1. Use list/dict comprehensions instead of multiple operations
2. Leverage built-in functions like max() for finding extremes
3. Use chain.from_iterable() for flattening sequences
4. Utilize isinstance() with tuple of types

Example transformations:

```python
# Instead of multiple set operations:
t_dags = {task.dag for task in tasks if not isinstance(task, tuple)}
t_dags_2 = {item[0].dag for item in tasks if isinstance(item, tuple)}
task_dags = t_dags | t_dags_2

# Use list comprehension:
task_dags = {
    task[0].dag if isinstance(task, tuple) else task.dag
    for task in tasks
}

# Instead of sorting and indexing:
items.sort(key=lambda x: x.end_date, reverse=True)
last_item = items[0] if items else None

# Use max():
last_item = max(items, key=lambda x: x.end_date) if items else None

# Instead of multiple isinstance checks:
if isinstance(log, chain) or isinstance(log, GeneratorType):
    ...

# Use tuple of types:
if isinstance(log, (chain, GeneratorType)):
    ...
```