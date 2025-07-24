---
title: Add logging without duplication
description: When adding logging functionality to existing code, encapsulate the logging
  logic within methods or use parameters to avoid code duplication and maintain clean
  interfaces. Add informational logging (debug/info level) to provide visibility into
  system operations, especially for default behaviors and skipped actions, but avoid
  duplicating conditional checks...
repository: docker/compose
label: Logging
language: Python
comments_count: 6
repository_stars: 35858
---

When adding logging functionality to existing code, encapsulate the logging logic within methods or use parameters to avoid code duplication and maintain clean interfaces. Add informational logging (debug/info level) to provide visibility into system operations, especially for default behaviors and skipped actions, but avoid duplicating conditional checks when the underlying methods already handle them.

For example, instead of duplicating logic across multiple code paths:
```python
# Bad - duplicated logging logic
if container.has_api_logs and not detached:
    container.attach_log_stream()
# ... repeated in multiple places

# Good - encapsulate in method parameters
self.start_container_if_stopped(container, attach_logs=not detached)
```

Also add debug logging for default behaviors that might not be obvious:
```python
# Good - inform about default file selection
log.debug("Using default config file: %s", winner)
```