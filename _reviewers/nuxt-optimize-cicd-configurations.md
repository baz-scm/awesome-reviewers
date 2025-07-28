---
title: optimize CI/CD configurations
description: Review CI/CD workflow configurations for both performance optimizations
  and accuracy in conditional logic. This includes minimizing resource usage where
  possible and ensuring all conditional statements use correct values.
repository: nuxt/nuxt
label: CI/CD
language: Yaml
comments_count: 2
repository_stars: 57769
---

Review CI/CD workflow configurations for both performance optimizations and accuracy in conditional logic. This includes minimizing resource usage where possible and ensuring all conditional statements use correct values.

For performance, avoid fetching unnecessary git history by using minimal fetch depth:
```yaml
- uses: actions/checkout@v4
  with:
    ref: ${{ steps.pr.outputs.head_sha }}
    fetch-depth: 1  # Only fetch the specific commit, not full history
```

For accuracy, verify that conditional statements reference correct repository names, environment variables, and other identifiers:
```yaml
if: ${{github.event_name == 'push' || github.repository == 'nuxt/nuxt'}}  # Correct repo name
```

These optimizations reduce build times, minimize resource consumption, and prevent workflow failures due to incorrect conditions.