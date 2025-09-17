---
title: Synchronize environment configurations
description: When making configuration changes, ensure all relevant environment files
  are updated consistently to prevent environment-specific inconsistencies and deployment
  issues.
repository: juspay/hyperswitch
label: Configurations
language: Toml
comments_count: 6
repository_stars: 34028
---

When making configuration changes, ensure all relevant environment files are updated consistently to prevent environment-specific inconsistencies and deployment issues.

Configuration changes should be propagated across all applicable files including:
- Development, sandbox, and production environment files
- Docker compose configurations  
- Example and template configuration files
- Environment-specific deployment configurations

Example of proper synchronization:
```toml
# If adding a new connector configuration in development.toml:
[newconnector]
base_url = "https://api-test.example.com/"

# Also update in:
# - sandbox.toml
# - production.toml (with production URL)
# - docker_compose.toml
# - config.example.toml (with documentation comments)
```

Always verify that configuration keys, formatting, and documentation comments remain consistent across all environment files. Pay special attention to URL formatting (trailing slashes), time unit specifications in comments, and naming conventions to maintain uniformity across environments.