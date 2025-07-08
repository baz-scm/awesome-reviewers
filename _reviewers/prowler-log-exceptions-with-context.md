---
title: Log exceptions with context
description: When handling exceptions in your code, ensure they are properly logged
  with sufficient context to aid debugging. For critical exceptions, use Sentry to
  track them alongside regular logging. For handled exceptions, include both the object
  being processed and the exception details in your log message.
repository: prowler-cloud/prowler
label: Logging
language: Python
comments_count: 2
repository_stars: 11834
---

When handling exceptions in your code, ensure they are properly logged with sufficient context to aid debugging. For critical exceptions, use Sentry to track them alongside regular logging. For handled exceptions, include both the object being processed and the exception details in your log message.

Example:
```python
try:
    result = process_item(item)
except Exception as exc:
    # For critical exceptions, capture in Sentry
    sentry_sdk.capture_exception(exc)
    
    # Always log with context information
    logger.warning(f"Failed to process '{item}': {exc}")
    
    # Then handle the exception appropriately
    # Don't silently continue without logging
```

Choose the appropriate log level based on severity - use error for application failures and warning for handled exceptions. Proper exception logging improves troubleshooting capabilities and helps identify recurring issues in production.