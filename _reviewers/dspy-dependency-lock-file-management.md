---
title: Dependency lock file management
description: Always commit dependency lock files (poetry.lock, package-lock.json,
  etc.) to version control and maintain their consistency across development environments.
  Lock files ensure reproducible builds and prevent environment mismatches that can
  cause unexpected changes or build failures.
repository: stanfordnlp/dspy
label: Configurations
language: Other
comments_count: 2
repository_stars: 27813
---

Always commit dependency lock files (poetry.lock, package-lock.json, etc.) to version control and maintain their consistency across development environments. Lock files ensure reproducible builds and prevent environment mismatches that can cause unexpected changes or build failures.

Before updating lock files, ensure your local environment matches the project's requirements by running the appropriate install command first. For Poetry projects, run `poetry install` before `poetry lock` to avoid introducing unrelated changes from environment mismatches.

Example workflow for Poetry:
```bash
# First, sync your environment with the existing lock file
poetry install

# Then update dependencies if needed
poetry lock

# Commit both pyproject.toml and poetry.lock
git add pyproject.toml poetry.lock
```

Never add lock files to .gitignore as they are essential for maintaining consistent dependency versions across all development and deployment environments.