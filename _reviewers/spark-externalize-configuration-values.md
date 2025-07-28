---
title: Externalize configuration values
description: Avoid hardcoding configuration values directly in code. Instead, make
  them externally configurable through appropriate mechanisms based on their usage
  patterns. Use environment variables for values that may need to change between deployments
  or runs, move configuration setup to appropriate lifecycle methods (like setupClass),
  and choose the right location...
repository: apache/spark
label: Configurations
language: Python
comments_count: 4
repository_stars: 41554
---

Avoid hardcoding configuration values directly in code. Instead, make them externally configurable through appropriate mechanisms based on their usage patterns. Use environment variables for values that may need to change between deployments or runs, move configuration setup to appropriate lifecycle methods (like setupClass), and choose the right location based on variability expectations.

For values that vary across runs of the same pipeline, use CLI arguments. For static pipeline configurations, use configuration files or specs. When possible, leverage built-in configuration mechanisms rather than implementing custom parsing.

Example of improvement:
```python
# Before: hardcoded retry count
exec_sbt(profiles_and_goals, retry=3)

# After: configurable via environment variable
retry_count = int(os.environ.get('SBT_RETRY_COUNT', '3'))
exec_sbt(profiles_and_goals, retry=retry_count)
```

This approach improves maintainability, reduces the need for code changes when configuration requirements change, and follows the principle that configuration should be external to code.