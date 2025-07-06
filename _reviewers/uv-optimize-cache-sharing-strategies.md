---
title: Optimize cache sharing strategies
description: 'Select the appropriate cache sharing approach based on your execution
  environment to maximize performance and efficiency. When working with containerized
  applications:'
repository: astral-sh/uv
label: Caching
language: Markdown
comments_count: 3
repository_stars: 60322
---

Select the appropriate cache sharing approach based on your execution environment to maximize performance and efficiency. When working with containerized applications:

1. For local development or long-running VMs:
   - Use cache mounts to persist the cache between container runs
   - Mount to the standard cache location (e.g., `~/.cache/uv`)

2. For CI environments (both parallel and sequential):
   - Use mounted volumes to share cache across containers
   - This reduces network traffic and speeds up dependency installation

Example for sharing cache in Docker containers:
```yaml
# Docker container cache sharing
volumes:
  - ./cache:/root/.cache/uv
```

Keep cache configurations simple by default and only add specialized invalidation patterns when necessary. For most cases, the default cache behavior is sufficient.