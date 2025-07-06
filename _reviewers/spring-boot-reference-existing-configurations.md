---
title: Reference existing configurations
description: When setting up configuration files, reference existing configuration
  sources rather than duplicating values or logic. This creates a single source of
  truth, reduces maintenance overhead, and prevents inconsistencies between different
  environments.
repository: spring-projects/spring-boot
label: Configurations
language: Yaml
comments_count: 3
repository_stars: 77637
---

When setting up configuration files, reference existing configuration sources rather than duplicating values or logic. This creates a single source of truth, reduces maintenance overhead, and prevents inconsistencies between different environments.

For example, when configuring tools that depend on version information that exists elsewhere in your project:

```yaml
# Instead of hardcoding Java version installation:
tasks:
  - init: yes | sdk install java && ./gradlew build

# Reference the version specified in .sdkmanrc:
tasks:
  - init: sdk env install && ./gradlew build
```

Similarly, when configuring service dependencies like health checks, prefer application-aware approaches over hardcoded values:

```yaml
# Instead of arbitrary wait times:
healthcheck:
  test: [ 'CMD', 'sleep', '115' ]

# Consider log pattern matching or status checks:
healthcheck:
  test: [ 'CMD', 'grep', '"Setup has completed"', '/var/log/application.log' ]
```

This approach ensures configuration changes only need to be made in one place and propagate automatically to dependent configurations, while also leveraging appropriate application-specific behaviors.