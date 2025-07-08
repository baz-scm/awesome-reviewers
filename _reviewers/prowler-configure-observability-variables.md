---
title: Configure observability variables
description: Always define all necessary environment variables for observability tools
  in configuration files, even if using default values. For error tracking services
  like Sentry, include both connection strings and contextual variables to ensure
  comprehensive error reporting. This improves troubleshooting by providing environment
  and release information with each...
repository: prowler-cloud/prowler
label: Observability
language: Other
comments_count: 2
repository_stars: 11834
---

Always define all necessary environment variables for observability tools in configuration files, even if using default values. For error tracking services like Sentry, include both connection strings and contextual variables to ensure comprehensive error reporting. This improves troubleshooting by providing environment and release information with each error.

```
# Error tracking configuration
DJANGO_SENTRY_DSN=
SENTRY_ENVIRONMENT=local
SENTRY_RELEASE=local
```