---
title: Pin dependency versions
description: Always specify exact versions of tools and dependencies in CI/CD workflows
  rather than using 'latest' or floating versions. This ensures build reproducibility,
  prevents unexpected failures when upstream dependencies change, and makes debugging
  easier.
repository: gin-gonic/gin
label: CI/CD
language: Yaml
comments_count: 2
repository_stars: 83022
---

Always specify exact versions of tools and dependencies in CI/CD workflows rather than using 'latest' or floating versions. This ensures build reproducibility, prevents unexpected failures when upstream dependencies change, and makes debugging easier.

Example:
```yml
# Instead of this (unstable):
- name: Setup golangci-lint
  uses: golangci/golangci-lint-action@v2
  with:
    version: latest

# Do this (stable):
- name: Setup golangci-lint
  uses: golangci/golangci-lint-action@v2
  with:
    version: v1.41.1
    args: --verbose
```

Similarly, when defining test matrices, explicitly specify all supported versions to ensure comprehensive coverage across environments.