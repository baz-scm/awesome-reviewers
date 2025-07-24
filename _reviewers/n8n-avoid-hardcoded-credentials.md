---
title: Avoid hardcoded credentials
description: Never hardcode sensitive information such as passwords, API keys, or
  authentication tokens in source code, configuration files, or container definitions.
  These can be exposed through version control systems, shared repositories, or compromised
  container images.
repository: n8n-io/n8n
label: Security
language: Dockerfile
comments_count: 1
repository_stars: 122978
---

Never hardcode sensitive information such as passwords, API keys, or authentication tokens in source code, configuration files, or container definitions. These can be exposed through version control systems, shared repositories, or compromised container images.

Instead:
1. Use environment variables or secure runtime configuration
2. Implement a secrets management solution
3. For Docker specifically, utilize build arguments that aren't persisted in the final image

Example - Instead of:
```dockerfile
FROM n8nio/n8n

ENV N8N_BASIC_AUTH_ACTIVE=true
ENV N8N_BASIC_AUTH_USER=Tre
ENV N8N_BASIC_AUTH_PASSWORD=Npt9854$
```

Better approach:
```dockerfile
FROM n8nio/n8n

ENV N8N_BASIC_AUTH_ACTIVE=true
# Credentials will be provided at runtime
# docker run -e N8N_BASIC_AUTH_USER=username -e N8N_BASIC_AUTH_PASSWORD=password n8n-image
```

For build-time configuration, use ARG instead of ENV for sensitive values that shouldn't persist in the image.