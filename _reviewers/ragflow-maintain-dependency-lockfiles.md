---
title: Maintain dependency lockfiles
description: 'When changing dependency declarations in configuration files like `pyproject.toml`,
  treat group placement and lockfile updates as part of the change.

  '
repository: infiniflow/ragflow
label: Configurations
language: Toml
comments_count: 2
repository_stars: 80174
---

When changing dependency declarations in configuration files like `pyproject.toml`, treat group placement and lockfile updates as part of the change.

- **Update/submit the lockfile** whenever dependencies or version constraints are modified (e.g., commit the corresponding `uv.lock`).
- **Preserve required dependency scope**: if a dependency is needed by multiple groups (such as both `default` and `test`), keep it declared in each required group—don’t “move” it to another group just to reduce duplication.

Example (pattern):
```toml
[project.optional-dependencies]
# Keep in both groups if both are required
default = ["pycryptodomex==3.20.0"]
test = ["pycryptodomex==3.20.0", "websockets>=14.0"]
```
After editing, regenerate and commit the matching lockfile (e.g., `uv.lock`).