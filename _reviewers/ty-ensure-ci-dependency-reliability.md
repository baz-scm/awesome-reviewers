---
title: Ensure CI dependency reliability
description: CI workflows should use the most current versions of dependencies and
  ensure all required tools are available. Avoid testing against potentially stale
  submodules or bundled dependencies by checking out the target repository directly.
  Use self-installing tools and hooks that handle their own installation to prevent
  failures due to missing dependencies.
repository: astral-sh/ty
label: CI/CD
language: Yaml
comments_count: 3
repository_stars: 11919
---

CI workflows should use the most current versions of dependencies and ensure all required tools are available. Avoid testing against potentially stale submodules or bundled dependencies by checking out the target repository directly. Use self-installing tools and hooks that handle their own installation to prevent failures due to missing dependencies.

For repository dependencies, checkout the actual target repository rather than a repo containing it as a submodule:

```yaml
- uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683 # v4.2.2
  with:
    persist-credentials: false
    repository: astral-sh/ruff  # Target repo, not the repo with submodule
```

For tool dependencies, prefer pre-commit hooks or actions that handle installation automatically:

```yaml
- repo: https://github.com/astral-sh/uv-pre-commit  # Self-installing hook
```

This approach ensures CI tests run against the latest code and don't fail due to missing tools, improving reliability and reducing maintenance overhead.