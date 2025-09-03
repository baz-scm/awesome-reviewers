---
title: Pin Docker base versions
description: Always specify exact version numbers for Docker base images instead of
  using floating tags like `lts` or `latest`. Floating tags can introduce unexpected
  breaking changes when they automatically update to newer versions, potentially causing
  build failures or runtime issues in production environments.
repository: lobehub/lobe-chat
label: Configurations
language: Dockerfile
comments_count: 2
repository_stars: 65138
---

Always specify exact version numbers for Docker base images instead of using floating tags like `lts` or `latest`. Floating tags can introduce unexpected breaking changes when they automatically update to newer versions, potentially causing build failures or runtime issues in production environments.

Use specific version tags that provide stability and predictable builds:

```dockerfile
# Good - pinned to specific version
FROM node:20-slim AS base

# Avoid - floating tag that can change unexpectedly  
FROM node:lts-slim AS base
```

While pinning versions, establish a regular review process to evaluate and upgrade to newer LTS versions when appropriate, ensuring your applications benefit from security updates and performance improvements without surprise breakages.