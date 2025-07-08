---
title: Reusable workflow design
description: Design CI/CD workflows with reusability and clear naming conventions
  from the start. Use meaningful prefixes that reflect the conceptual purpose (like
  "trunk" for trunk-based development), and consider future extraction into standalone,
  parameterized actions when similar functionality might be needed across repositories.
repository: pytorch/pytorch
label: CI/CD
language: Yaml
comments_count: 3
repository_stars: 91345
---

Design CI/CD workflows with reusability and clear naming conventions from the start. Use meaningful prefixes that reflect the conceptual purpose (like "trunk" for trunk-based development), and consider future extraction into standalone, parameterized actions when similar functionality might be needed across repositories.

For workflow implementation:
1. Choose meaningful, consistent naming conventions
2. Make key values configurable via input parameters
3. Use consistent package management approaches with explicit flags

Example:
```yaml
name: reusable-build-workflow

on:
  workflow_call:
    inputs:
      commit_sha:
        description: 'Commit SHA to build (leave empty for current HEAD)'
        required: false
        type: string
      prefix:
        description: 'Tag prefix to use (e.g. trunk)'
        required: true
        type: string

jobs:
  build:
    steps:
      - name: Set variables
        id: vars
        run: |
          COMMIT_SHA="${{ inputs.commit_sha || github.sha }}"
          echo "tag_name=${{ inputs.prefix }}/${COMMIT_SHA}" >> $GITHUB_OUTPUT
      
      # For package installation, use consistent approach with explicit flags
      - name: Install dependencies
        run: pip install cmake --force-reinstall
```

This approach makes workflows more maintainable and enables cross-repository sharing of common CI/CD patterns.