---
title: Version pre-bump for releases
description: When your release workflow automatically bumps versions (e.g., increments
  the patch number), do not set the manifest version to the final release you want.
  Instead, set it to the documented pre-bump “magic” value so the workflow transforms
  it into the intended release.
repository: awslabs/mcp
label: CI/CD
language: Toml
comments_count: 2
repository_stars: 9545
---

When your release workflow automatically bumps versions (e.g., increments the patch number), do not set the manifest version to the final release you want. Instead, set it to the documented pre-bump “magic” value so the workflow transforms it into the intended release.

How to apply:
- Update version fields in build/release manifests (e.g., `pyproject.toml`) using the pre-bump value.
- Treat the final version as something produced by CI/CD, not something you directly commit.
- If you want release `X.Y.Z`, compute the manifest version so that after the workflow’s patch bump it lands on `X.Y.Z`.

Example (using the pre-bump value from the project):
```toml
[project]
name = "awslabs.example"
# Want the workflow to produce version 1.1.0
version = "1.0.9223372036854775807"

# Want the workflow to produce version 2.1.0
version = "2.0.9223372036854775807"
```
If you set `version = "1.1.0"` (or `"2.1.0"`) directly while the workflow bumps the patch, the release will come out one patch higher than intended.