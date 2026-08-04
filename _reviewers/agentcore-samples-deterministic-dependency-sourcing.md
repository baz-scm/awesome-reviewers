---
title: Deterministic dependency sourcing
description: 'All CI/CD build environments must be reproducible and based on reliable
  dependency sources.


  Standards:

  1) Prefer official published packages/artifacts'
repository: awslabs/agentcore-samples
label: CI/CD
language: Other
comments_count: 2
repository_stars: 3244
---

All CI/CD build environments must be reproducible and based on reliable dependency sources.

Standards:
1) Prefer official published packages/artifacts
- In build files (Dockerfiles, pipelines), install dependencies from the official package index/SDK rather than custom/local wheel (.whl) files.
- Only allow custom wheels/artifacts when there is a clear, documented reason (e.g., temporary feature/variant or missing optional dependency), and include a time-bounded plan to replace them with the official SDK.

2) Always pin dependency versions in CI/CD
- Commit and use the project’s lockfile (e.g., uv.lock) so both direct and transitive dependencies are locked for the exact commit.
- Avoid strategies that implicitly pull “latest” versions during builds.

Example (Dockerfile pattern)
```dockerfile
FROM --platform=linux/arm64 python:3.12-slim
WORKDIR /app

# Install deterministic dependencies
COPY uv.lock ./
# (Use your project’s standard lock-based install command; e.g.,)
# RUN uv sync --frozen

# Prefer the official SDK package instead of a custom wheel
# RUN pip install strands-<version>[bidi]
```

How to apply:
- If you’re tempted to install from a custom .whl, first check whether the official SDK already supports your needed configuration; if not, require a documented exception and an explicit “replace with official” follow-up.
- If a lockfile is proposed for removal, verify the pipeline can still guarantee pinned transitive dependencies; typically it cannot, so keep it and use it in the build.