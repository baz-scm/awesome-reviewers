---
title: Pin problematic dependencies
description: When external dependencies or tools in CI/CD pipelines have known regressions
  or bugs, pin them to stable versions and document the reasoning with issue links.
  Include TODO comments to track when temporary measures can be reverted.
repository: remix-run/react-router
label: CI/CD
language: Yaml
comments_count: 2
repository_stars: 55270
---

When external dependencies or tools in CI/CD pipelines have known regressions or bugs, pin them to stable versions and document the reasoning with issue links. Include TODO comments to track when temporary measures can be reverted.

This prevents CI/CD pipeline failures and ensures build stability while maintaining visibility into when constraints can be lifted.

Example:
```yaml
# PLEASE KEEP THIS PINNED TO 1.4.10 to avoid a regression in 1.5.*
# See https://github.com/changesets/action/issues/465
uses: changesets/action@v1.4.10

# TODO: Track and re-enable once this has been fixed: https://github.com/google/wireit/issues/1297
# - uses: google/wireit@setup-github-actions-caching/v2
```

Always include the specific issue URL and a clear explanation of what regression or problem the pinning/disabling prevents.