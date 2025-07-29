---
title: Centralize configuration values
description: Avoid duplicating configuration values across multiple files by maintaining
  a single source of truth for environment variables, build arguments, version specifications,
  and other configuration parameters. When the same value appears in build scripts,
  Dockerfiles, documentation, or configuration files, consolidate it to one authoritative
  location and...
repository: apache/kafka
label: Configurations
language: Dockerfile
comments_count: 2
repository_stars: 30575
---

Avoid duplicating configuration values across multiple files by maintaining a single source of truth for environment variables, build arguments, version specifications, and other configuration parameters. When the same value appears in build scripts, Dockerfiles, documentation, or configuration files, consolidate it to one authoritative location and reference it from other places using placeholders or variables.

This prevents inconsistencies that arise when updating configuration values, reduces maintenance overhead, and eliminates inaccurate or stale configuration data that becomes outdated during rebuilds or updates.

Example of the problem:
```dockerfile
# In Dockerfile - duplicated default value
ARG jdk_version=openjdk:17-bullseye

# In build script - same default value duplicated
DEFAULT_JDK=openjdk:17-bullseye
```

Better approach:
```dockerfile
# In Dockerfile - no default, relies on build script
ARG jdk_version

# In README.md - use placeholder
FROM <JDK_IMAGE>
```

Also avoid configuration values that become inaccurate over time, such as hardcoded build dates in environment variables that don't reflect actual rebuild times.