---
title: avoid hardcoded credentials
description: Never embed sensitive credentials, passwords, API keys, or other secrets
  directly in source code. Hardcoded credentials create security vulnerabilities by
  exposing sensitive data in version control systems and making it accessible to anyone
  with code access.
repository: BerriAI/litellm
label: Security
language: Yaml
comments_count: 1
repository_stars: 28310
---

Never embed sensitive credentials, passwords, API keys, or other secrets directly in source code. Hardcoded credentials create security vulnerabilities by exposing sensitive data in version control systems and making it accessible to anyone with code access.

Instead, use secure alternatives:
- Environment variables for local development
- Secret management systems (GitHub Secrets, AWS Secrets Manager, etc.)
- Configuration files that are excluded from version control

Example of what to avoid:
```yaml
cache_params:
  type: "redis"
  host: "redis-18438.c277.us-east-1-3.ec2.redns.redis-cloud.com"
  port: 18438
  password: "hB44ThYlB4W4m7wpCUwrSzteHqvDKnDV"  # ❌ Hardcoded password
```

Better approach:
```yaml
cache_params:
  type: "redis"
  host: "redis-18438.c277.us-east-1-3.ec2.redns.redis-cloud.com"
  port: 18438
  password: ${REDIS_PASSWORD}  # ✅ Environment variable
```

This practice protects against credential leaks and ensures sensitive data remains secure across different deployment environments.