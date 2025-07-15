---
title: Parameterize version requirements
description: Always parameterize tool and runtime versions in CI/CD configurations
  rather than hardcoding them. This makes your pipelines more maintainable when dependencies
  need updates and provides a single source of truth for version requirements.
repository: nestjs/nest
label: CI/CD
language: Yaml
comments_count: 3
repository_stars: 71767
---

Always parameterize tool and runtime versions in CI/CD configurations rather than hardcoding them. This makes your pipelines more maintainable when dependencies need updates and provides a single source of truth for version requirements.

For critical dependencies like Node.js or package managers:
1. Define versions as parameters at the top of your configuration
2. Reference these parameters throughout your configuration
3. Consider separate parameters for maintenance and legacy versions
4. Use version ranges when appropriate to get compatible updates

Example:
```yaml
# Good practice
parameters:
  maintenance-node-version:
    type: string
    default: "16.20"
  
jobs:
  build:
    docker:
      - image: cimg/node:<< pipeline.parameters.maintenance-node-version >>
    steps:
      - run:
          command: 'npm install -g npm@^8'  # Version range for compatible updates
```

This approach helps prevent CI failures when new incompatible versions are released and simplifies the process of updating dependencies across multiple workflow steps.