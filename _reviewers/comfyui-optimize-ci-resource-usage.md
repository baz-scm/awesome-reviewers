---
title: optimize CI resource usage
description: Design CI/CD workflows to minimize unnecessary resource consumption and
  provide faster feedback. Avoid triggering builds when changes don't impact the build
  output, use appropriate event triggers, and implement clean artifact management
  strategies.
repository: comfyanonymous/ComfyUI
label: CI/CD
language: Yaml
comments_count: 5
repository_stars: 83726
---

Design CI/CD workflows to minimize unnecessary resource consumption and provide faster feedback. Avoid triggering builds when changes don't impact the build output, use appropriate event triggers, and implement clean artifact management strategies.

Key practices:
- Use conditional triggers or path filters to avoid building when changes don't affect the build (e.g., documentation-only changes shouldn't trigger Docker builds)
- Choose appropriate workflow triggers - prefer `release: types: [published]` for production deployments rather than building on every branch push
- Implement clean tagging strategies to avoid registry pollution - use `type=edge,branch=master` instead of `type=ref,event=branch` and avoid unnecessary tags like `type=sha` or `type=ref,event=pr`
- Reduce timeout values for faster failure detection (e.g., reduce wait times from 10 minutes to 30 seconds)
- Consider matrix complexity - support only variants with known demand rather than "every platform that a compiler supports just because they can"

Example of efficient workflow triggers:
```yaml
on:
  release:
    types: [published]  # Only build on actual releases
  push:
    branches: [master]
    paths-ignore: ['docs/**', '*.md']  # Skip builds for doc changes
```

This approach reduces CI costs, speeds up feedback loops, and prevents resource waste while maintaining necessary build coverage.