---
title: Validate nulls explicitly
description: Always check for null values before using them, and use Python's idiomatic
  patterns to make these checks concise and readable. This prevents unexpected errors
  and makes code more maintainable.
repository: apache/airflow
label: Null Handling
language: Python
comments_count: 5
repository_stars: 40858
---

Always check for null values before using them, and use Python's idiomatic patterns to make these checks concise and readable. This prevents unexpected errors and makes code more maintainable.

There are several approaches to handle null values effectively:

1. **Explicit validation before use:**
   ```python
   # Instead of:
   url = cast("str", conn.schema) + "://" + cast("str", conn.host)
   
   # Do this:
   if conn.schema is None:
       raise AirflowException("Schema field is missing and is required.")
   if conn.host is None:
       raise AirflowException("Host field is missing and is required.")
   url = conn.schema + "://" + conn.host
   ```

2. **Use the walrus operator for concise null checking:**
   ```python
   # Instead of:
   processor = self._processors.pop(proc, None)
   if processor:
       processor.logger_filehandle.close()
   
   # Use:
   if processor := self._processors.pop(proc, None):
       processor.logger_filehandle.close()
   ```

3. **Avoid TYPE_CHECKING asserts for nullability:**
   ```python
   # Instead of:
   dag_version = DagVersion.get_latest_version(dag.dag_id, session=session)
   if TYPE_CHECKING:
       assert dag_version
       
   # Do proper null checking:
   dag_version = DagVersion.get_latest_version(dag.dag_id, session=session)
   if dag_version is None:
       raise ValueError(f"No version found for DAG {dag.dag_id}")
   ```

4. **Understand return types:**
   When a function should always return a valid value (like a list, even if empty), don't add unnecessary null checks that suggest the function might return None.

Proper null handling improves code readability, prevents common runtime errors, and makes intentions clear to both humans and static analysis tools.