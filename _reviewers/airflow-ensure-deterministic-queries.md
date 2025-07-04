---
title: Ensure deterministic queries
description: 'Build SQLAlchemy queries that are both efficient and deterministic to
  prevent unpredictable results and improve performance. When writing database queries:'
repository: apache/airflow
label: Database
language: Python
comments_count: 4
repository_stars: 40858
---

Build SQLAlchemy queries that are both efficient and deterministic to prevent unpredictable results and improve performance. When writing database queries:

1. **Use SQLAlchemy's native operators** instead of Python's bitwise operators for better readability:
```python
# Instead of this:
query.where((DagFavorite.dag_id == DagModel.dag_id) & (DagFavorite.user_id == self.user_id))

# Use this:
query.where(and_(DagFavorite.dag_id == DagModel.dag_id, DagFavorite.user_id == self.user_id))
```

2. **Build queries with explicit control flow** for complex conditions:
```python
# Instead of adding a complex boolean expression:
query = ...
since_running = Log.dttm > last_running_time if last_running_time else True
query = query.where(Log.event == EVENT, since_running)

# Prefer explicit conditional logic:
query = query.where(Log.event == EVENT)
if last_running_time:
    query = query.where(Log.dttm > last_running_time)
```

3. **Always ensure deterministic ordering** by including a unique identifier (typically the primary key) as a secondary sort criterion:
```python
# Instead of:
query.order_by(AssetEvent.timestamp.asc())

# Use:
query.order_by(AssetEvent.timestamp.asc(), AssetEvent.id.asc())
```

4. **Review query filters carefully** to avoid overly restrictive WHERE clauses that might unintentionally exclude valid records. Consider the complete range of valid states and values that should be included in your results.