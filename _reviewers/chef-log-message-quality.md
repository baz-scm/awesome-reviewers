---
title: Log message quality
description: Ensure all log messages are consistent in formatting and clear in purpose.
  Complete sentences in logs should end with proper punctuation (especially periods),
  and messages should precisely describe what is happening in the system. When logging
  phase transitions or significant events, explicitly state where one phase ends and
  another begins rather than using...
repository: chef/chef
label: Logging
language: Markdown
comments_count: 2
repository_stars: 7860
---

Ensure all log messages are consistent in formatting and clear in purpose. Complete sentences in logs should end with proper punctuation (especially periods), and messages should precisely describe what is happening in the system. When logging phase transitions or significant events, explicitly state where one phase ends and another begins rather than using vague descriptions.

Example:
```ruby
# Poor logging
logger.info("Processing data")
logger.info("Infra Phase and Compliance Phase improved")

# Better logging
logger.info("Processing data.")
logger.info("Transitioning from Infra Phase to Compliance Phase.")
```

This standard improves log readability during troubleshooting and ensures documentation accurately reflects system behavior.
