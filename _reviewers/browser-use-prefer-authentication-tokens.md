---
title: prefer authentication tokens
description: When configuring authentication in CI/CD workflows, prefer using tokens
  over passwords for enhanced security. Tokens can be scoped with specific permissions,
  rotated more easily, and provide better audit trails compared to passwords. This
  is particularly important for service-to-service authentication where credentials
  are stored as secrets.
repository: browser-use/browser-use
label: Security
language: Yaml
comments_count: 1
repository_stars: 69139
---

When configuring authentication in CI/CD workflows, prefer using tokens over passwords for enhanced security. Tokens can be scoped with specific permissions, rotated more easily, and provide better audit trails compared to passwords. This is particularly important for service-to-service authentication where credentials are stored as secrets.

For Docker Hub authentication in GitHub Actions, use a personal access token instead of your account password:

```yaml
- name: Log in to Docker Hub
  uses: docker/login-action@v3
  with:
    username: ${{ secrets.DOCKER_USERNAME }}
    password: ${{ secrets.DOCKER_TOKEN }}  # Use token instead of password
```

Even when official documentation shows password usage, prioritize token-based authentication as it follows security best practices and reduces the risk of credential compromise.