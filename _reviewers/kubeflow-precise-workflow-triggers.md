---
title: Precise workflow triggers
description: Configure CI/CD workflows to trigger precisely based on relevant file
  path changes. This minimizes unnecessary builds and tests while ensuring all required
  workflows run when dependencies are modified.
repository: kubeflow/kubeflow
label: CI/CD
language: Yaml
comments_count: 7
repository_stars: 15064
---

Configure CI/CD workflows to trigger precisely based on relevant file path changes. This minimizes unnecessary builds and tests while ensuring all required workflows run when dependencies are modified.

**For component-specific workflows:**
- Include both direct component paths and shared dependencies
- For web applications, include common library paths

```yaml
# Example for a web application workflow
name: Build & Publish JWA Docker image
on:
  push:
    branches:
      - master
      - v*-branch
    paths:
      - components/crud-web-apps/jupyter/**      # Component code
      - components/crud-web-apps/common/**       # Shared dependencies
```

**For manifest-related workflows:**
- Target only specific manifest directories rather than all component files

```yaml
# For manifest testing, specify manifest paths only
name: Build Profile Controller manifests
on:
  pull_request:
    paths:
      - components/profile-controller/config/**  # Only manifest changes
```

Centralize build logic in Makefiles instead of duplicating in GitHub Actions. This allows workflows to simply call make targets, making pipelines more maintainable and consistent across environments.
