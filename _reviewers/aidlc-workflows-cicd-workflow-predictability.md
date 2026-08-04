---
title: CI/CD Workflow Predictability
description: 'When configuring GitHub Actions for CI/CD, keep workflow outputs and
  triggers predictable:


  1) Use safe, stable identifiers for artifacts/reports. Don’t build artifact names
  from values that can be invalid (e.g., raw branch/ref names). Prefer constants or
  explicitly sanitized values.'
repository: awslabs/aidlc-workflows
label: CI/CD
language: Yaml
comments_count: 2
repository_stars: 3849
---

When configuring GitHub Actions for CI/CD, keep workflow outputs and triggers predictable:

1) Use safe, stable identifiers for artifacts/reports. Don’t build artifact names from values that can be invalid (e.g., raw branch/ref names). Prefer constants or explicitly sanitized values.

Example (stable artifact name):
```yaml
# Prefer a constant over potentially invalid dynamic ref names
name: "report-head"
# In expressions:
# format('report-head')
```

2) Don’t redundantly declare default PR trigger types. For `on: pull_request`, `opened`, `reopened`, and `synchronize` are defaults—specify only the additional types you actually need (e.g., `labeled`).

Example:
```yaml
on:
  pull_request:
    branches: [main]
    types:
      - labeled  # add only non-default events
```