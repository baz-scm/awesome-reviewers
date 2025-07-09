---
title: Pin environment versions
description: Always use explicit version tags for CI/CD environments (runners, containers,
  images, tool versions) instead of floating references like 'latest'. This practice
  prevents unexpected breakages when upstream environments are updated and gives the
  team control over when to upgrade. When upgrading is necessary, do it in a dedicated
  PR to properly test the...
repository: vitessio/vitess
label: CI/CD
language: Yaml
comments_count: 2
repository_stars: 19815
---

Always use explicit version tags for CI/CD environments (runners, containers, images, tool versions) instead of floating references like 'latest'. This practice prevents unexpected breakages when upstream environments are updated and gives the team control over when to upgrade. When upgrading is necessary, do it in a dedicated PR to properly test the changes without blocking other development work.

Example:
```yaml
jobs:
  build:
    # Good: Explicitly pinned version
    runs-on: ubuntu-22.04
    
    # Avoid: Floating version tag
    # runs-on: ubuntu-latest
    
  test:
    container:
      # Good: Pinned image version
      image: python:3.11.4
      
      # Avoid: Floating tag
      # image: python:latest
```