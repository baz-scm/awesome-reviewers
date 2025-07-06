---
title: Use appropriate logging levels
description: Select the correct logging level based on the importance and visibility
  requirements of the information. Choose WARNING for issues that should be visible
  by default and may require attention, INFO for general operational messages, and
  DEBUG for detailed information needed only during troubleshooting. Additionally,
  ensure log messages include sufficient...
repository: bridgecrewio/checkov
label: Logging
language: Python
comments_count: 5
repository_stars: 7668
---

Select the correct logging level based on the importance and visibility requirements of the information. Choose WARNING for issues that should be visible by default and may require attention, INFO for general operational messages, and DEBUG for detailed information needed only during troubleshooting. Additionally, ensure log messages include sufficient context to be meaningful on their own.

Example:
```python
# Good - Using warning for issues that should be visible by default
logging.warning(f"Resource dependency {processed_dep} not found in {dep}")

# Good - Using debug for detailed information with context
logging.debug(f"OpenAI request returned: {completion}")

# Good - Using info with specific context about what's being processed
logging.info(f"Done persisting {len(maps)} maps to {bucket}/{key}")

# Good - Using logging framework instead of print statements
logging.info(f"Authentication failed for user {username}")

# Avoid - Using info for detailed debug information
# logging.info(f"[COMPLETION]{completion}")

# Avoid - Vague messages without context
# logging.warning("Dependency not found")

# Avoid - Using print statements
# print(f"Authentication failed for user {username}")
```

When deciding between log levels, consider both the importance of the message and how it will be used. Warning logs should be used for situations that aren't errors but may require attention, while debug logs should contain information helpful for troubleshooting without cluttering normal operation logs.