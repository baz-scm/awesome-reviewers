---
title: Secure credential management
description: Never hardcode sensitive information like passwords, API keys, or access
  tokens directly in code or configuration files (including Dockerfiles). These credentials
  can be exposed through version control systems, shared images, or when files are
  accessed by unauthorized users.
repository: n8n-io/n8n
label: Security
language: Txt
comments_count: 1
repository_stars: 122978
---

Never hardcode sensitive information like passwords, API keys, or access tokens directly in code or configuration files (including Dockerfiles). These credentials can be exposed through version control systems, shared images, or when files are accessed by unauthorized users.

Instead:
- Use environment variables to inject sensitive values at runtime
- Implement Docker secrets for container deployments
- Utilize secure credential management systems for storing sensitive information

Example - Insecure:
```dockerfile
# Dockerfile.prod
FROM nginx:latest
ENV ADMIN_PASSWORD=supersecret123
```

Example - Secure:
```dockerfile
# Dockerfile.prod
FROM nginx:latest
ENV ADMIN_PASSWORD=${ADMIN_PASSWORD}
# Password will be passed at build/runtime, not stored in file
```