---
title: optimize CI/CD pipelines
description: 'CI/CD pipelines should be optimized for both performance and maintainability
  through strategic caching, script consolidation, and compilation optimization. This
  involves three key practices:'
repository: LMCache/LMCache
label: CI/CD
language: Shell
comments_count: 3
repository_stars: 3800
---

CI/CD pipelines should be optimized for both performance and maintainability through strategic caching, script consolidation, and compilation optimization. This involves three key practices:

1. **Implement proper caching strategies**: Use comprehensive cache keys that include build identifiers and dependency checksums to ensure cache invalidation works correctly. For environment caching, include unique build IDs to prevent stale cache reuse.

2. **Consolidate related scripts**: Minimize the number of separate bash scripts by merging related functionality. This reduces maintenance overhead and simplifies pipeline complexity as the project grows.

3. **Optimize compilation performance**: Implement compilation caching (like ccache) for projects with significant build times to improve pipeline speed.

Example cache configuration:
{% raw %}
```yaml
plugins:
  - cache#v1.5.2:
      key: "venv-{{ BUILDKITE_BUILD_ID }}-{{ checksum \"requirements/common.txt\" }}-{{ checksum \"requirements/test.txt\" }}"
      path: ".venv"
      save: "pipeline"
      force: true
```
{% endraw %}

These optimizations ensure CI/CD pipelines remain fast, reliable, and maintainable as projects scale.
