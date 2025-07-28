---
title: Remove unsupported runtime versions
description: When maintaining CI/CD pipelines, regularly audit and remove runtime
  versions that are no longer supported by your project's dependencies or cause build
  failures. This prevents pipeline instability and reduces maintenance overhead.
repository: google-gemini/gemini-cli
label: CI/CD
language: Yaml
comments_count: 3
repository_stars: 65062
---

When maintaining CI/CD pipelines, regularly audit and remove runtime versions that are no longer supported by your project's dependencies or cause build failures. This prevents pipeline instability and reduces maintenance overhead.

Unsupported versions should be removed from all workflow matrices consistently across test, integration, and end-to-end testing jobs to maintain pipeline reliability.

Example:
```yaml
strategy:
  matrix:
    # Remove 18.x due to dependency compatibility issues
    node-version: [20.x, 22.x, 24.x]
```

This practice ensures that CI resources are focused on supported runtime environments and prevents false negatives from incompatible version combinations. When removing versions, document the reasoning (e.g., "dependency requires Node 20+") to help future maintainers understand the decision.