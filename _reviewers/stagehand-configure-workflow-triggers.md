---
title: Configure workflow triggers
description: Ensure GitHub Actions workflows are triggered appropriately by configuring
  branch patterns and path filters to balance CI efficiency with comprehensive coverage.
  Workflows should run on all relevant branches (not just main) while using path filters
  to avoid unnecessary executions.
repository: browserbase/stagehand
label: CI/CD
language: Yaml
comments_count: 3
repository_stars: 16443
---

Ensure GitHub Actions workflows are triggered appropriately by configuring branch patterns and path filters to balance CI efficiency with comprehensive coverage. Workflows should run on all relevant branches (not just main) while using path filters to avoid unnecessary executions.

Configure triggers to run on pushes to any branch when you need broad coverage:
```yaml
on:
  push:
    branches: ["*"]  # or specific patterns like "dev/*"
```

Use path filters to limit runs to relevant file changes:
```yaml
on:
  push:
    branches: ["*"]
    paths:
      - "lib/**"
      - "evals/**"
```

Avoid overly restrictive triggers that only run on main branch, as this prevents catching issues early in the development cycle. Consider that some changes (like types) may be caught by other build processes (tsc, eslint) and don't always need separate CI runs.