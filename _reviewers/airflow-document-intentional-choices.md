---
title: Document intentional choices
description: 'Add explanatory comments for non-obvious code decisions that might appear
  incorrect, unusual, or suboptimal to future contributors. Without such comments,
  code that looks unusual might be "fixed" during refactoring, introducing bugs. This
  is particularly important for:'
repository: apache/airflow
label: Documentation
language: Python
comments_count: 3
repository_stars: 40858
---

Add explanatory comments for non-obvious code decisions that might appear incorrect, unusual, or suboptimal to future contributors. Without such comments, code that looks unusual might be "fixed" during refactoring, introducing bugs. This is particularly important for:

- Deliberate error handling patterns
- Usage of internal/private methods
- Explicit attributes that could be detected automatically 
- Performance trade-offs

For example:

```python
# Deliberately returning 403 without details to avoid information leakage
raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token")

# Using _get_response() only for initial message where parent sends unsolicited data
msg = comms_decoder._get_response()

# Explicit attribute definition to prevent automatic detection which would be error-prone
dependent_tables: list[str] | None = None
```

These comments explain the "why" behind code decisions that might not be immediately obvious, preventing well-intentioned changes that could break intended behavior.