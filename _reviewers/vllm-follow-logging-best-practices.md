---
title: Follow logging best practices
description: 'Maintain high-quality logging throughout the codebase by following these
  best practices:


  1. **Use appropriate log levels**: Reserve `debug` for detailed troubleshooting,
  `info` for general operational information, `warning` for potential issues, and
  `error`/`critical` for actual problems. Avoid excessive logging at higher levels.'
repository: vllm-project/vllm
label: Logging
language: Python
comments_count: 7
repository_stars: 51730
---

Maintain high-quality logging throughout the codebase by following these best practices:

1. **Use appropriate log levels**: Reserve `debug` for detailed troubleshooting, `info` for general operational information, `warning` for potential issues, and `error`/`critical` for actual problems. Avoid excessive logging at higher levels.
   ```python
   # For large object dumps or detailed diagnostics
   logger.debug("Initialized config %s", config)
   # Not: logger.info("Initialized config %s", config)
   ```

2. **Remove temporary debugging logs**: Debug statements with developer identifiers (e.g., `"[Kourosh]"`) should be removed before merging code.

3. **Optimize logging performance**: Guard expensive parameter computations to avoid unnecessary work when the log level is disabled:
   ```python
   if logger.isEnabledFor(logging.DEBUG):
       logger.debug("Complex calculation result: %s", 
                    ",".join(map(str, complex_calculation())))
   ```

4. **Avoid logging in loops** unless each iteration provides unique valuable information. Consider logging summaries before/after the loop instead.

5. **Use standard logging methods**: Use `logger.warning()` (not the deprecated `logger.warn()`), and use `logger.exception()` for exception logging to automatically include tracebacks:
   ```python
   try:
       # Some operation
   except Exception:
       logger.exception("Failed to perform operation")
       # Not: logger.error("Failed: %s", str(e))
   ```

6. **Initialize loggers consistently**: Use the project's standard logger initialization pattern:
   ```python
   from vllm.logger import init_logger
   logger = init_logger(__name__)
   ```

7. **Make log messages clear and actionable**: Include relevant context and avoid ambiguous messages.