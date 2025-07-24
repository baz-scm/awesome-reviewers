---
title: Sync environment variables
description: When converting hardcoded values to environment variables in configuration
  files (like docker-compose.yml), always update corresponding example files (e.g.,
  .env.example) with appropriate default values. This ensures that developers can
  use standard setup processes without additional manual configuration.
repository: supabase/supabase
label: Configurations
language: Yaml
comments_count: 2
repository_stars: 86070
---

When converting hardcoded values to environment variables in configuration files (like docker-compose.yml), always update corresponding example files (e.g., .env.example) with appropriate default values. This ensures that developers can use standard setup processes without additional manual configuration.

Example:
```diff
# In docker-compose.yml
- SECRET_KEY_BASE=UpNVntn3cDxHJpq99YMc1T1AQgQpc8kfYTuRgBiYa15BLrx8etQoXz3gZv1/u2oq
+ SECRET_KEY_BASE=${POOLER_SECRET_KEY_BASE}

# You must also update .env.example
+ POOLER_SECRET_KEY_BASE=UpNVntn3cDxHJpq99YMc1T1AQgQpc8kfYTuRgBiYa15BLrx8etQoXz3gZv1/u2oq
```

This maintains compatibility for new developers setting up the project and prevents broken workflows when someone runs `cp .env.example .env && docker-compose up`.