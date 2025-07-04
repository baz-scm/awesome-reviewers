---
title: Context-rich log messages
description: Ensure log messages provide clear context about what happened, potential
  consequences, and actionable information for debugging. Choose appropriate log levels
  based on severity, and include exception details when catching errors.
repository: apache/airflow
label: Logging
language: Python
comments_count: 4
repository_stars: 40858
---

Ensure log messages provide clear context about what happened, potential consequences, and actionable information for debugging. Choose appropriate log levels based on severity, and include exception details when catching errors.

Good log messages significantly improve troubleshooting efficiency by providing developers with information needed to understand issues without requiring code examination.

Examples:
```python
# Instead of vague messages:
log.warning("Failed to get user name from os: %s", e)

# Provide context about impact:
log.warning("Failed to get user name from os: %s, not setting the triggering user", e)

# When handling exceptions, log the full exception:
try:
    sqs_get_queue_attrs_response = self.sqs_client.get_queue_attributes(
        QueueUrl=queue_url, AttributeNames=["ApproximateNumberOfMessages"]
    )
    # Process response...
except Exception as e:
    # Include details for better debugging
    log.error("SQS connection health check failed: %s", e)
```

Consider what information would be most helpful to developers trying to diagnose an issue from logs alone.