---
title: CI conditional job handling
description: When implementing CI workflows with path-based filtering, ensure that
  conditional jobs don't inadvertently block PR merges when they don't execute. Maintain
  proper path filtering to run jobs only when relevant files change, but account for
  scenarios where filtered jobs are listed as required dependencies.
repository: calcom/cal.com
label: CI/CD
language: Yaml
comments_count: 2
repository_stars: 37732
---

When implementing CI workflows with path-based filtering, ensure that conditional jobs don't inadvertently block PR merges when they don't execute. Maintain proper path filtering to run jobs only when relevant files change, but account for scenarios where filtered jobs are listed as required dependencies.

For workflows with path filtering, use `if` conditions or separate the conditional jobs from required job lists to prevent blocking PRs that don't trigger those specific workflows.

Example of problematic configuration:
```yaml
# atoms-e2e.yml - runs only on specific paths
on:
  pull_request:
    paths:
      - 'packages/atoms/**'

# pr.yml - requires atoms job even when it doesn't run
jobs:
  required-checks:
    needs: [
      e2e-embed,
      e2e-atoms,  # This blocks PRs when atoms-e2e doesn't run
    ]
```

Instead, handle conditional dependencies appropriately by either using conditional requirements or separating path-specific jobs from universal requirements.