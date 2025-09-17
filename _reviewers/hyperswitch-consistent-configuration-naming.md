---
title: consistent configuration naming
description: Configuration variable names should follow consistent patterns and be
  descriptive enough to clearly convey their purpose and scope. When naming similar
  configuration parameters, maintain uniform naming conventions throughout the codebase.
repository: juspay/hyperswitch
label: Naming Conventions
language: Toml
comments_count: 2
repository_stars: 34028
---

Configuration variable names should follow consistent patterns and be descriptive enough to clearly convey their purpose and scope. When naming similar configuration parameters, maintain uniform naming conventions throughout the codebase.

For time-based configuration parameters, explicitly indicate the time scope in the variable name. Use consistent patterns like `max_retries_per_day` and `max_retries_last_30_days` rather than mixing formats like `max_daily_retry_count` and `retry_count_30_day`.

Example of improved naming:
```toml
# Instead of:
max_daily_retry_count = 3
retry_count_30_day = 20

# Use:
max_retries_per_day = 3
max_retries_last_30_days = 20
```

This approach makes configuration files more readable and reduces confusion when developers need to understand or modify these settings. Consistent naming patterns also make it easier to search for and group related configuration parameters.