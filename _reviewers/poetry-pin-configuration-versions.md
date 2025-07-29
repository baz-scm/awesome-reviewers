---
title: Pin configuration versions
description: Always pin specific versions for base images, dependencies, and environment
  configurations to ensure reproducible builds and prevent unexpected failures from
  upstream changes.
repository: python-poetry/poetry
label: Configurations
language: Dockerfile
comments_count: 3
repository_stars: 33496
---

Always pin specific versions for base images, dependencies, and environment configurations to ensure reproducible builds and prevent unexpected failures from upstream changes.

When configuring Docker images, development containers, or dependency management tools, specify exact versions rather than using generic tags like "latest" or broad version ranges. This prevents builds from breaking when upstream maintainers release new versions or change default behaviors.

Example from Docker configurations:
```dockerfile
# Instead of generic versions
FROM python:3

# Use pinned versions
FROM python:3.11-slim-bookworm

# Pin dependency versions
ARG POETRY_VERSION=1.8
RUN pip install "poetry==${POETRY_VERSION}"
```

This practice is especially critical for:
- Base Docker images (pin both Python version and OS distribution)
- Package manager versions (Poetry, pip, etc.)
- Development container images
- CI/CD environments

The small overhead of occasionally updating pinned versions is far outweighed by the stability and predictability gained, particularly when upstream changes can introduce security vulnerabilities or breaking changes that affect your build process.