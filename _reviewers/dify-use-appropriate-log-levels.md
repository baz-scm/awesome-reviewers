---
title: Use appropriate log levels
description: Choose the correct logging level based on the importance and purpose
  of the message. Use DEBUG for debugging information that's only useful during development,
  INFO for general operational information, WARNING for concerning conditions that
  don't prevent operation, and ERROR for actual errors. Remove meaningless debug prints
  and consider using conditional...
repository: langgenius/dify
label: Logging
language: Python
comments_count: 6
repository_stars: 114231
---

Choose the correct logging level based on the importance and purpose of the message. Use DEBUG for debugging information that's only useful during development, INFO for general operational information, WARNING for concerning conditions that don't prevent operation, and ERROR for actual errors. Remove meaningless debug prints and consider using conditional logging for expensive operations.

Examples:
- Use DEBUG for detailed debugging: `if logger.isEnabledFor(logging.DEBUG): logger.debug("Detailed debug info")`
- Use WARNING for concerning conditions: `logger.warning("Document not found, skipping processing")`
- Remove debug prints: `logging.error(f"{dataset_id_str}")` should be removed or changed to appropriate level
- Use INFO for operational messages: `logger.info("Created workflow alias: %s for workflow %s", alias_name, workflow_id)`

Avoid leaving temporary debug logs in production code and ensure log levels match the actual significance of the information being logged.