---
title: Configure loggers consistently
description: Always configure module-level loggers with a consistent pattern across
  the codebase. Use `logging.getLogger(__name__)` to create loggers that match the
  module hierarchy, set appropriate default levels (typically WARNING for library
  code), use standardized formatting that includes timestamp, logger name, level,
  and message, and provide mechanisms to adjust...
repository: salesforce/cloudsplaining
label: Logging
language: Python
comments_count: 2
repository_stars: 2100
---

Always configure module-level loggers with a consistent pattern across the codebase. Use `logging.getLogger(__name__)` to create loggers that match the module hierarchy, set appropriate default levels (typically WARNING for library code), use standardized formatting that includes timestamp, logger name, level, and message, and provide mechanisms to adjust log levels at runtime.

Example:
```python
import logging
import sys

# Create module-level logger with consistent naming
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)  # Set default level to WARNING

# Configure handler and formatter consistently
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Provide a way to adjust log level at runtime
def change_log_level(log_level):
    logger.setLevel(log_level)
```

This approach ensures logs are consistent across the application, properly namespaced, and can be controlled for verbosity based on runtime needs (like command line flags).