---
title: Pin dependency versions
description: Explicitly pin or constrain dependency versions in CI/CD configurations
  instead of using `latest` tags. This prevents unexpected build failures when new
  incompatible versions are released. Consider using parameterized versions to centralize
  version management while maintaining stability.
repository: nestjs/nest
label: CI/CD
language: Yaml
comments_count: 4
repository_stars: 71766
---

Explicitly pin or constrain dependency versions in CI/CD configurations instead of using `latest` tags. This prevents unexpected build failures when new incompatible versions are released. Consider using parameterized versions to centralize version management while maintaining stability.

For tool installations in CI pipelines:
```yaml
# Avoid this:
- run:
    name: Update NPM version
    command: 'sudo npm install -g npm@latest'

# Prefer this:
- run:
    name: Update NPM version
    command: 'sudo npm install -g npm@^8'

# Or better, use parameters:
parameters:
  npm-version:
    type: string
    default: "^8"
  
jobs:
  build:
    # ...
    steps:
      - run:
          name: Update NPM version
          command: 'sudo npm install -g npm@<< pipeline.parameters.npm-version >>'
```

For GitHub Actions or other external dependencies, specify exact versions or follow a semantic versioning strategy that matches your risk tolerance. Consider establishing a regular process to review and update dependency versions.