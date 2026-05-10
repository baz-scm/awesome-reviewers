---
title: Explicit dependency constraints
description: 'In configuration/requirements files, make compatibility explicit: bound
  versions to prevent silent breakage across Python/platform build environments, and
  use environment markers for dependencies that differ by Python version, OS, implementation,
  or wheel availability.'
repository: celery/celery
label: Configurations
language: Txt
comments_count: 8
repository_stars: 28464
---

In configuration/requirements files, make compatibility explicit: bound versions to prevent silent breakage across Python/platform build environments, and use environment markers for dependencies that differ by Python version, OS, implementation, or wheel availability.

Do:
- Prefer bounded ranges that preserve compatibility, e.g. `package>=x.y,<x.(y+1)` or `~=x.y` when appropriate.
- Use environment markers when a dependency must vary by `python_version`, `sys_platform`, or `platform_python_implementation`.
- Constrain build-tooling for known breakpoints (e.g., `setuptools<82.0.0` when source builds fail with newer setuptools).
- Justify pins (`==`) only when you must avoid known incompatibilities or missing wheels; otherwise prefer ranges.

Don’t:
- Rely on overly broad constraints that can change behavior between build environments.
- Swap `<=` to `==` without a clear motivation (it’s a silent change for users depending on transitive compatibility).

Example pattern:
```txt
# Tooling broken beyond a known version for certain builds
setuptools<82.0.0

# Different tooling versions per Python
pre-commit>=3.5.0,<3.8.0; python_version < '3.9'
pre-commit>=3.8.0; python_version >= '3.9'

# Platform/implementation gating for deps without universal wheels/support
pycurl>=7.43.0.5; sys_platform != 'win32' and platform_python_implementation=="CPython"

# Major-version safety constraints for runtime libs
cassandra-driver>=3.24,<4
```