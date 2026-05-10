---
title: Config-Accurate Dependency Management
description: 'When updating project configuration (e.g., `pyproject.toml`), ensure
  dependency declarations match how packages are actually used: align `requires-python`
  with dependency-supported Python versions, keep dev-only tooling in `dev-dependencies`,
  and use `extras` for optional features instead of adding new required runtime deps.
  Also, set minimum versions based...'
repository: openai/openai-python
label: Configurations
language: Toml
comments_count: 4
repository_stars: 30731
---

When updating project configuration (e.g., `pyproject.toml`), ensure dependency declarations match how packages are actually used: align `requires-python` with dependency-supported Python versions, keep dev-only tooling in `dev-dependencies`, and use `extras` for optional features instead of adding new required runtime deps. Also, set minimum versions based on the concrete APIs/helpers you rely on.

Apply this checklist:
- Python compatibility: if any dependency requires `Python>=X`, set `requires-python` to at least `>=X` (don’t claim broader support than your deps allow).
- Dependency grouping: packages used only for tests/build/tooling go in `dev-dependencies`, not `dependencies`.
- Optional features via extras: move feature-specific packages to an extra (e.g., `openai[cli]`) and load them safely at the call site.
- Minimum versions: bump `>=` versions when the features you use are introduced/changed in newer upstream releases.

Example (optional CLI dependency):
```toml
# pyproject.toml
[project.optional-dependencies]
cli = ["argcomplete>=1.12.0"]
```
```py
# _cli.py
try:
    import argcomplete  # type: ignore
except ImportError:
    argcomplete = None

if argcomplete is not None:
    # use argcomplete
    ...
else:
    # either disable CLI niceties or show a message
    ...
```
