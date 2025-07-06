---
title: Optimize docker build caching
description: Leverage Docker BuildKit's cache and bind mount capabilities to dramatically
  improve CI build times and reduce image sizes. Instead of copying source files into
  intermediate layers, use bind mounts to provide build context and cache mounts for
  package managers and build artifacts.
repository: astral-sh/uv
label: CI/CD
language: Dockerfile
comments_count: 2
repository_stars: 60322
---

Leverage Docker BuildKit's cache and bind mount capabilities to dramatically improve CI build times and reduce image sizes. Instead of copying source files into intermediate layers, use bind mounts to provide build context and cache mounts for package managers and build artifacts.

**Why this matters:**
- Prevents bloating Docker layer cache with source files and build artifacts
- Significantly reduces build times in CI/CD pipelines
- Makes builds more consistent and reliable

**Implementation example:**
```dockerfile
# Use cache mounts for package managers
RUN \
  --mount=target=/var/lib/apt/lists,type=cache,sharing=locked \
  --mount=target=/var/cache/apt,type=cache,sharing=locked \
  <<HEREDOC
    apt update && apt install -y --no-install-recommends \
      build-essential \
      curl
HEREDOC

# Use bind mounts for source files and cache mounts for build artifacts
RUN \
  --mount=type=bind,source=src,target=src \
  --mount=type=bind,source=package.json,target=package.json \
  --mount=type=cache,target=node_modules \
  npm install && npm run build
```

Make sure your CI environment supports BuildKit (Docker 18.09+) and enable BuildKit features with `DOCKER_BUILDKIT=1`.