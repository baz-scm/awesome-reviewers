---
title: Least Privilege CI Permissions
description: In CI/CD (e.g., GitHub Actions), follow least-privilege for the built-in
  `GITHUB_TOKEN`. Avoid granting broad, workflow-wide permissions. Default to no permissions
  at the top level, then explicitly grant only what a specific job needs.
repository: awslabs/mcp
label: Security
language: Yaml
comments_count: 1
repository_stars: 9545
---

In CI/CD (e.g., GitHub Actions), follow least-privilege for the built-in `GITHUB_TOKEN`. Avoid granting broad, workflow-wide permissions. Default to no permissions at the top level, then explicitly grant only what a specific job needs.

Example (deny by default, allow only when required):

```yaml
name: Example

on:
  push:
    branches: [main]

# Deny by default
permissions: {}

jobs:
  sync-something:
    runs-on: ubuntu-latest

    # Grant only the minimum needed by this job
    permissions:
      contents: write
      pull-requests: write

    steps:
      - uses: actions/checkout@v4
      # ...
```

Apply this rule by reviewing each workflow and ensuring any write permissions (`contents`, `pull-requests`, etc.) are scoped to the smallest possible job/step and granted only if truly necessary.