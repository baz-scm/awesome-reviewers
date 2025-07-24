---
title: Never commit credentials
description: Credentials, passwords, API tokens, and database connection strings must
  never be committed to version control in any form, even in configuration files or
  Kubernetes manifests. This practice exposes sensitive information to anyone with
  repository access and creates security vulnerabilities.
repository: n8n-io/n8n
label: Security
language: Yaml
comments_count: 3
repository_stars: 122978
---

Credentials, passwords, API tokens, and database connection strings must never be committed to version control in any form, even in configuration files or Kubernetes manifests. This practice exposes sensitive information to anyone with repository access and creates security vulnerabilities.

Instead:
1. Use environment variables or secret injection at runtime
2. Store credentials in a dedicated secrets management system
3. Include placeholders in configuration files

Example - Replace hardcoded credentials:

```yaml
# INSECURE - Don't do this
MONGODB_URI: "mongodb+srv://akaneai420:ilovehentai123@cluster0.jwyab3g.mongodb.net/?retryWrites=true"
LOGIN_PASSWORD: password

# SECURE - Do this instead
MONGODB_URI: "${MONGODB_URI}"
LOGIN_PASSWORD: ${LOGIN_PASSWORD}
```

For Kubernetes, use secrets management solutions rather than committing stringData values directly. When committing example configurations, always use placeholder values that make it clear a real value needs to be substituted.