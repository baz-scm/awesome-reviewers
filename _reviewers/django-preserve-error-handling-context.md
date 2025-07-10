---
title: Preserve error handling context
description: 'When handling exceptions, preserve the original error context and provide
  clear, actionable error messages. This helps with debugging and improves the developer
  experience. Key practices:'
repository: django/django
label: Error Handling
language: Python
comments_count: 5
repository_stars: 84182
---

When handling exceptions, preserve the original error context and provide clear, actionable error messages. This helps with debugging and improves the developer experience. Key practices:

1. Avoid swallowing exception details during serialization or logging
2. Include specific information about what caused the error
3. Use appropriate exception types for different error scenarios
4. Consider adding fallback error representations

Example of good error handling:

```python
def handle_task_error(exc):
    try:
        # Attempt full error serialization
        return {
            "error_type": type(exc).__name__,
            "error_details": str(exc),
            "traceback": "".join(format_exception(type(exc), exc, exc.__traceback__)),
        }
    except Exception:
        # Fallback to basic error information if serialization fails
        return {
            "error_type": type(exc).__name__,
            "error_message": str(exc),
            "note": "Full error details unavailable - serialization failed"
        }
```

This approach ensures that error information is preserved as much as possible, with a fallback mechanism when full details cannot be captured. It helps maintain debuggability while being robust against serialization or logging failures.