---
title: CI workflow optimization
description: Optimize CI/CD workflows by prioritizing reliability over convenience
  and leveraging built-in platform features. When workflows generate files or have
  complex dependencies, use brute-force approaches like `make clean; make` to ensure
  reproducible builds, even if it seems inefficient. Simplify workflow steps by using
  native GitHub Actions features instead of...
repository: semgrep/semgrep
label: CI/CD
language: Yaml
comments_count: 4
repository_stars: 12598
---

Optimize CI/CD workflows by prioritizing reliability over convenience and leveraging built-in platform features. When workflows generate files or have complex dependencies, use brute-force approaches like `make clean; make` to ensure reproducible builds, even if it seems inefficient. Simplify workflow steps by using native GitHub Actions features instead of manual workarounds - for example, use `submodules: true` in checkout actions rather than separate submodule checkout steps.

Look for opportunities to consolidate similar workflows that perform redundant operations, as this can reduce maintenance overhead and improve build times. When making dependency changes, consider the overall impact on workflow performance and whether jobs can be parallelized or merged.

Example of reliable build verification:
```yaml
- name: Check GitHub workflow files are up to date
  working-directory: .github/workflows
  run: |
    sudo apt-get update
    sudo apt-get install jsonnet
    make clean  # Ensure clean state
    make        # Regenerate all files
```

Example of using built-in features:
```yaml
- uses: actions/checkout@v3
  with:
    submodules: true  # Instead of separate checkout steps
```