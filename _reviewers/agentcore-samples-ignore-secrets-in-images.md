---
title: Ignore secrets in images
description: When building container images, never copy the entire build context blindly.
  Add a `.dockerignore` (and/or use targeted `COPY` paths) to ensure sensitive files
  and local artifacts can’t be baked into the image—especially when using `COPY .
  .`.
repository: awslabs/agentcore-samples
label: Security
language: Dockerfile
comments_count: 1
repository_stars: 3244
---

When building container images, never copy the entire build context blindly. Add a `.dockerignore` (and/or use targeted `COPY` paths) to ensure sensitive files and local artifacts can’t be baked into the image—especially when using `COPY . .`.

Practical standard:
- Always exclude: `.env`, `.venv/`, `__pycache__/`, `*.pyc` (and other environment/credential files).
- Prefer `COPY requirements.txt ./` then install, and only copy the needed source directories.

Example `.dockerignore`:
```dockerignore
.env
.venv/
__pycache__/
*.pyc
```