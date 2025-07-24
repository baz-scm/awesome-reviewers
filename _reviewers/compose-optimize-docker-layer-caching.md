---
title: optimize Docker layer caching
description: Order Dockerfile instructions from least frequently changing to most
  frequently changing to maximize Docker layer caching efficiency and reduce build
  times in CI/CD pipelines.
repository: docker/compose
label: CI/CD
language: Dockerfile
comments_count: 2
repository_stars: 35858
---

Order Dockerfile instructions from least frequently changing to most frequently changing to maximize Docker layer caching efficiency and reduce build times in CI/CD pipelines.

Place stable elements like base images, system packages, and dependency installations early in the Dockerfile. Move frequently changing elements like source code copies, environment variables used only at runtime, and build artifacts toward the end.

Example of proper ordering:
```dockerfile
# Stable base and dependencies first
FROM python:3.7.3-alpine3.9 AS build
RUN apk add --no-cache gcc git make

# Less frequently changing files
COPY requirements.txt .
COPY setup.py .
RUN pip install -r requirements.txt

# More frequently changing source code
COPY . .

# Runtime-specific variables last
ARG GIT_COMMIT=unknown
ENV DOCKER_COMPOSE_GITSHA=$GIT_COMMIT
RUN script/build/linux-entrypoint
```

This approach prevents cache invalidation of expensive operations like package installations when only source code changes, significantly improving CI/CD build performance.