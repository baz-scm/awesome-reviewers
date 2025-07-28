---
title: Document network configuration
description: When configuring network settings in containerized services, always document
  the reasoning behind specific choices, especially for port mappings and security-related
  flags. This helps other developers understand the configuration and prevents accidental
  misconfigurations.
repository: prisma/prisma
label: Networking
language: Yaml
comments_count: 2
repository_stars: 42967
---

When configuring network settings in containerized services, always document the reasoning behind specific choices, especially for port mappings and security-related flags. This helps other developers understand the configuration and prevents accidental misconfigurations.

For port mappings, use reasonable external port numbers and explain any non-standard choices:
```yaml
ports:
  - 9432:5432 # Postgres port - using 9432 to avoid conflicts
```

For network security flags, document their purpose and security implications:
```yaml
healthcheck:
  test: ['CMD', '/opt/mssql-tools18/bin/sqlcmd', '-C', '-Usa', '-PPr1sm4_Pr1sm4', '-Q', 'select 1']
  # -C flag trusts server certificate without validation
```

This practice prevents confusion during deployment and helps maintain consistent network configuration across environments.