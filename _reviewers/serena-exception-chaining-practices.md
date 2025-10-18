---
title: Exception chaining practices
description: Always use exception chaining with `raise ... from e` when re-raising
  or wrapping exceptions to preserve the original error context and stack trace. This
  maintains debugging information and follows Python best practices for error propagation.
repository: oraios/serena
label: Error Handling
language: Python
comments_count: 4
repository_stars: 14465
---

Always use exception chaining with `raise ... from e` when re-raising or wrapping exceptions to preserve the original error context and stack trace. This maintains debugging information and follows Python best practices for error propagation.

When catching and re-raising exceptions, avoid losing the original exception context. Exception chaining helps developers trace the root cause of errors through the entire call stack.

Example of proper exception chaining:
```python
try:
    project_config = ProjectConfig.from_yml(Path(project_file_path))
except Exception as e:
    raise ValueError(f"Error loading project configuration from {project_file_path}: {e}") from e
```

Additionally, catch specific exception types rather than broad parent classes to avoid unintended behavior. For instance, catch `PermissionError` specifically rather than its parent `OSError` when you only want to handle permission issues.

Avoid over-decorating exceptions with unnecessary context when the original exception already contains sufficient information for debugging.