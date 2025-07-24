---
title: Synchronize configuration values
description: 'Ensure all configuration values, particularly version numbers and environment
  variables, are consistent across related files to prevent subtle bugs and deployment
  issues. When updating configurations:'
repository: appwrite/appwrite
label: Configurations
language: Other
comments_count: 6
repository_stars: 51959
---

Ensure all configuration values, particularly version numbers and environment variables, are consistent across related files to prevent subtle bugs and deployment issues. When updating configurations:

1. Identify all related occurrences of the same value across different files (e.g., docker-compose.yml, .phtml templates)
2. Update all instances to use the same value or parameter
3. For renamed variables, remove the deprecated ones to prevent ambiguity
4. When backward compatibility is needed, explicitly support both legacy and current values

Example for version synchronization:
```diff
# In app/views/install/compose.phtml
- image: openruntimes/executor:0.7.14
+ image: openruntimes/executor:0.7.16  # Match version in docker-compose.yml
```

Example for environment variables:
```diff
# Remove deprecated variable to avoid confusion
-      - _APP_MAINTENANCE_DELAY
       - _APP_MAINTENANCE_START_TIME
```

Example for maintaining backward compatibility:
```diff
# Support both legacy and current runtime versions
- OPR_EXECUTOR_RUNTIME_VERSIONS=v5
+ OPR_EXECUTOR_RUNTIME_VERSIONS=v2,v5
```