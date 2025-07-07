---
title: Minimize configuration complexity
description: 'Keep configuration files clean and maintainable by regularly reviewing
  and removing unnecessary settings and outdated version support. This includes:

  '
repository: gin-gonic/gin
label: Configurations
language: Yaml
comments_count: 2
repository_stars: 83022
---

Keep configuration files clean and maintainable by regularly reviewing and removing unnecessary settings and outdated version support. This includes:

1. Remove environment variables that are no longer required in newer versions of tools or languages
2. Drop support for legacy versions that require special configuration or lack compatibility with modern tooling

Example from Go configuration:
```yaml
# Good practice - only set environment variables when needed
matrix:
  - go: 1.12.x
    env: GO111MODULE=on
  - go: 1.13.x
    # No GO111MODULE needed for 1.13+ as it's the default behavior
```

When evaluating which configurations to keep, consider:
- Is this setting still required for the latest versions?
- Does maintaining support for older versions add unnecessary complexity?
- Are there newer conventions or defaults that make explicit configuration redundant?

Regular audits of configuration files prevent accumulation of outdated settings and help maintain a cleaner, more understandable development environment.