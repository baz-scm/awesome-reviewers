---
title: Parameterize configuration values
description: Always extract configuration values (like versions, paths, or other changeable
  settings) into parameters rather than hardcoding them directly in multiple places.
  This creates a single source of truth, simplifies updates, and makes your code more
  maintainable.
repository: prowler-cloud/prowler
label: Configurations
language: Dockerfile
comments_count: 2
repository_stars: 11834
---

Always extract configuration values (like versions, paths, or other changeable settings) into parameters rather than hardcoding them directly in multiple places. This creates a single source of truth, simplifies updates, and makes your code more maintainable.

For Dockerfiles, use ARG directives:

```Dockerfile
# Good practice
ARG POWERSHELL_VERSION=7.5.0

# Later used as:
RUN curl -L https://github.com/PowerShell/PowerShell/releases/download/v${POWERSHELL_VERSION}/powershell-${POWERSHELL_VERSION}-linux-x64.tar.gz
```

Consider whether configurations should be controlled through environment variables or build arguments, based on when and how they need to be modified. For critical components like dependency versions, implementing a single source of truth ensures consistency across your application and simplifies future updates.