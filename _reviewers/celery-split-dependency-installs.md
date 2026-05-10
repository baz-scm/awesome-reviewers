---
title: Split Dependency Installs
description: 'When building Docker images, optimize dependency installation for both
  caching and resource limits.


  Apply these rules:

  1) **Maximize layer caching:** install Python requirements *before* copying your
  application source.'
repository: celery/celery
label: Performance Optimization
language: Dockerfile
comments_count: 3
repository_stars: 28464
---

When building Docker images, optimize dependency installation for both caching and resource limits.

Apply these rules:
1) **Maximize layer caching:** install Python requirements *before* copying your application source.
2) **Cache package downloads:** use BuildKit cache mounts for pip to avoid re-downloading on rebuilds.
3) **Bound resource usage:** split large multi-version dependency installs into separate `RUN` steps (avoid one massive chained install) to prevent `ResourceExhausted` and reduce memory pressure.

Example pattern (mimics the discussed approach):
```dockerfile
# Define pyenv versions
RUN pyenv local 3.13 3.12 3.11 3.10 3.9 3.8 pypy3.10

# Install requirements first for layer caching
RUN --mount=type=cache,target=/home/$CELERY_USER/.cache/pip \
    pyenv exec python3.13 -m pip install -r requirements/default.txt \
    -r requirements/dev.txt -r requirements/docs.txt

RUN --mount=type=cache,target=/home/$CELERY_USER/.cache/pip \
    pyenv exec python3.12 -m pip install -r requirements/default.txt \
    -r requirements/dev.txt -r requirements/docs.txt

# Copy app after deps
COPY --chown=1000:1000 . $HOME/celery

# Install app last (optionally with --no-deps since deps are already installed)
RUN --mount=type=cache,target=/home/$CELERY_USER/.cache/pip \
    pyenv exec python3.13 -m pip install --no-deps -e $HOME/celery
```

If a single combined install step causes `ResourceExhausted`, keep (or further refine) the split into smaller `RUN` layers. Ensure toolchain setup used by dependency builds is deterministic and architecture-aware to avoid rebuild failures across environments.