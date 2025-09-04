---
title: Use standardized logging pattern
description: Always use the standardized logging pattern with module-level loggers
  instead of print statements or direct logging calls. This ensures consistent logging
  behavior, proper log level control, and better debugging capabilities across the
  codebase.
repository: stanfordnlp/dspy
label: Logging
language: Python
comments_count: 4
repository_stars: 27813
---

Always use the standardized logging pattern with module-level loggers instead of print statements or direct logging calls. This ensures consistent logging behavior, proper log level control, and better debugging capabilities across the codebase.

The standard pattern is:
```python
import logging

logger = logging.getLogger(__name__)
logger.info("Your message here")
logger.warning("Warning message")
logger.debug("Debug info", exc_info=True)  # Include exception info when relevant
```

Replace print statements with appropriate log levels:
- Use `logger.error()` or `logger.warning()` instead of `print(e)` for exceptions
- Use `logger.info()` for general information
- Use `logger.debug()` for detailed debugging information

In modules where the dspy logger isn't available (like dsp folder), follow the same pattern by creating a module-level logger. This maintains consistency and allows proper log level configuration across the entire application.