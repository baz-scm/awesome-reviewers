---
title: Externalize configuration values
description: Configuration files should not contain hardcoded values for usernames,
  credentials, hostnames, or environment-specific settings. Instead, use environment
  variables, templated values, or dynamic references that can adapt to different deployment
  contexts.
repository: elie222/inbox-zero
label: Configurations
language: Yaml
comments_count: 3
repository_stars: 8267
---

Configuration files should not contain hardcoded values for usernames, credentials, hostnames, or environment-specific settings. Instead, use environment variables, templated values, or dynamic references that can adapt to different deployment contexts.

This approach improves:
- **Security**: Prevents credentials from being checked into source control
- **Portability**: Allows configurations to work across different environments
- **Collaboration**: Makes it easier for teams to work on the same codebase without conflicts

For Docker and CI/CD configurations:
```diff
# In docker-compose.yml
- DATABASE_URL: "postgresql://postgres:password@db:5432/inboxzero?schema=public"
+ DATABASE_URL: ${DATABASE_URL:-postgresql://${POSTGRES_USER:-postgres}:${POSTGRES_PASSWORD}@db:5432/${POSTGRES_DB:-inboxzero}?schema=public}

# In GitHub workflows
- DOCKER_USERNAME: "elie222"
+ DOCKER_USERNAME: "${{ github.repository_owner }}"

# In Docker images
- image: ghcr.io/elie222/inbox-zero:latest
+ image: ghcr.io/${ORGANIZATION:-$USER}/inbox-zero:latest
```

For sensitive values, consider using secrets management systems for production environments. For local development, provide `.env.example` files as templates that developers can copy to create their own `.env` files, which should be excluded from version control.