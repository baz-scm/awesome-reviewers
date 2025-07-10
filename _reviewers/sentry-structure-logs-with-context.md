---
title: Structure logs with context
description: 'Use structured logging with appropriate context and log levels to maximize
  the value of log messages. Include relevant metadata with each log message to facilitate
  filtering and debugging:'
repository: getsentry/sentry
label: Logging
language: Python
comments_count: 6
repository_stars: 41297
---

Use structured logging with appropriate context and log levels to maximize the value of log messages. Include relevant metadata with each log message to facilitate filtering and debugging:

1. Use structured logging patterns that allow consistent inclusion of contextual information:
   ```python
   # Instead of:
   logger.info("Processing item")
   
   # Do this:
   logger.info("Processing item", extra={"project_id": project.id, "item_type": item.type})
   
   # Or with Sentry SDK:
   sentry_sdk.set_context("operation_context", {"project_id": project.id, "item_type": item.type})
   ```

2. Choose log levels based on actionability:
   - ERROR: For actionable issues requiring immediate attention
   - WARNING: For potential problems that may need attention
   - INFO: For general operational information
   - DEBUG: For detailed troubleshooting information
   
   Instead of removing logging statements, consider lowering their level to DEBUG for infrequently needed information.

3. When logging exceptions:
   - Include both error type and message
   - Preserve stack traces using `logger.exception()` or `exc_info=True`
   - For lower severity issues, use appropriate level with context:
   ```python
   try:
       # operation
   except ApiError as e:
       # For non-critical errors that don't need immediate action
       logger.warning("API operation failed", exc_info=True, extra={"operation": "fetch_data"})
       # Or with Sentry:
       sentry_sdk.set_context("operation_context", {"operation": "fetch_data"})
       sentry_sdk.capture_exception(error=e, level="warning")
   ```

4. Avoid duplicate logging. If using a framework that handles logging (like lifecycle), add context to it rather than creating separate log entries:
   ```python
   # Instead of:
   lifecycle.record_halt(reason)
   logger.info("Operation halted", extra={"reason": reason})
   
   # Do this:
   lifecycle.add_extras({"project_id": project.id})
   lifecycle.record_halt(reason)
   ```

Following these practices improves troubleshooting efficiency, enables better log filtering, and ensures that logs provide maximum value for debugging production issues.