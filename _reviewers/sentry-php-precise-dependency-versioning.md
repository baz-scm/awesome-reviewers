---
title: Precise dependency versioning
description: When specifying dependency version constraints in configuration files,
  be deliberate about minimum versions based on required features and compatibility
  requirements. Use the lowest compatible version constraint to maximize project compatibility,
  but ensure specific feature requirements are met.
repository: getsentry/sentry-php
label: Configurations
language: Json
comments_count: 4
repository_stars: 1873
---

When specifying dependency version constraints in configuration files, be deliberate about minimum versions based on required features and compatibility requirements. Use the lowest compatible version constraint to maximize project compatibility, but ensure specific feature requirements are met.

For example, if your code requires a specific feature added in version 1.6 of a package:

```json
// Good - Specific minimum version based on feature requirements
"monolog/monolog": "^1.6|^2.0|^3.0",

// Bad - Unnecessarily restrictive
"monolog/monolog": "^1.3|^2.0",
```

When upgrading dependency versions, consider broader compatibility impacts with other packages in your ecosystem. Use version ranges (e.g., `^2.19|^3.4`) when necessary to maintain compatibility with different environments. Document the reasoning for specific version constraints when they're not obvious, especially when choosing a particular minimum version for feature availability.