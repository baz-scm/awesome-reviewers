---
title: Pin CI dependencies securely
description: Always pin CI/CD dependencies (GitHub Actions, external tools) to specific
  commit hashes or exact versions rather than using floating tags like @v1 or @latest.
  This prevents supply chain attacks and ensures reproducible builds. However, pinned
  dependencies must be regularly updated to avoid using outdated or vulnerable versions.
repository: ant-design/ant-design
label: CI/CD
language: Yaml
comments_count: 2
repository_stars: 95882
---

Always pin CI/CD dependencies (GitHub Actions, external tools) to specific commit hashes or exact versions rather than using floating tags like @v1 or @latest. This prevents supply chain attacks and ensures reproducible builds. However, pinned dependencies must be regularly updated to avoid using outdated or vulnerable versions.

For GitHub Actions, use commit hashes with descriptive comments:

```yaml
- name: verify-version
  uses: actions-cool/verify-files-modify@82e88fd0e8e5ed5b7f1a9e6a3c4b9c2d1234567 # pin to latest verified commit
```

When implementing automated dependency updates, ensure proper token permissions are configured so that generated PRs can run CI checks. This allows safe validation of dependency changes before merging. Consider using tokens with minimal required permissions rather than default tokens to maintain security while enabling necessary CI functionality.