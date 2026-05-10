---
title: Environment-consistent builds
description: 'When building/installing Python dependencies in Docker/CI for multiple
  Python versions, keep the environment deterministic and aligned across interpreters:
  use the same dependency constraint/lock inputs everywhere and ensure the packaging
  toolchain is consistent per interpreter.'
repository: celery/celery
label: Configurations
language: Dockerfile
comments_count: 3
repository_stars: 28464
---

When building/installing Python dependencies in Docker/CI for multiple Python versions, keep the environment deterministic and aligned across interpreters: use the same dependency constraint/lock inputs everywhere and ensure the packaging toolchain is consistent per interpreter.

Apply this by:
- Always pass the shared constraints/lock file to pip installs (for every supported Python/PyPy build).
- Before installing requirements, upgrade `pip`, `setuptools`, and `wheel` using the target interpreter.
- Keep configuration formatting consistent (e.g., Docker `ENV KEY=VALUE` style) to avoid lint/tooling drift.

Example (adapted):
```dockerfile
RUN pyenv exec python3.11 -m pip install --upgrade pip setuptools wheel \
 && --mount=type=cache,target=/home/$CELERY_USER/.cache/pip \
    pyenv exec python3.11 -m pip install -r requirements/test.txt \
      --build-constraint requirements/constraints.txt

# Prefer consistent ENV syntax
ENV PYTHONUNBUFFERED=1
ENV PYTHONIOENCODING=UTF-8
```