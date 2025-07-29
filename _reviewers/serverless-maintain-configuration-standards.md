---
title: maintain configuration standards
description: Ensure configuration files maintain both consistency and currency across
  all services. Configuration values should follow established patterns within the
  codebase and use up-to-date versions for runtimes and dependencies.
repository: serverless/serverless
label: Configurations
language: Yaml
comments_count: 2
repository_stars: 46810
---

Ensure configuration files maintain both consistency and currency across all services. Configuration values should follow established patterns within the codebase and use up-to-date versions for runtimes and dependencies.

Key practices:
- Apply consistent validation modes across all service configurations (e.g., `configValidationMode: error`)
- Keep runtime versions current and avoid outdated versions
- Review configuration files for both standardization and version currency

Example from serverless.yml:
```yaml
service: my-service

configValidationMode: error  # Consistent validation across services

provider:
  name: aws
  runtime: nodejs16.x  # Use current runtime versions, not nodejs12.x
```

This ensures reliable deployments and reduces configuration drift between services while maintaining security and compatibility with current platform features.