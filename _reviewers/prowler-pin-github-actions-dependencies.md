---
title: Pin GitHub Actions dependencies
description: Always pin GitHub Actions to specific commit SHAs rather than using major
  version references to prevent supply chain attacks and ensure workflow stability.
  This practice ensures your CI/CD pipelines remain consistent and secure even if
  the referenced action is updated or compromised.
repository: prowler-cloud/prowler
label: CI/CD
language: Yaml
comments_count: 3
repository_stars: 11834
---

Always pin GitHub Actions to specific commit SHAs rather than using major version references to prevent supply chain attacks and ensure workflow stability. This practice ensures your CI/CD pipelines remain consistent and secure even if the referenced action is updated or compromised.

**Example:**
```yaml
# Instead of this (vulnerable to supply chain attacks):
- name: Find existing changelog comment
  uses: peter-evans/find-comment@v3

# Use this (pinned to specific SHA and version):
- name: Find existing changelog comment
  uses: peter-evans/find-comment@3eae4d37986fb5a8592848f6a574fdf654e61f9e #v3.1.0
```

Additionally, when implementing workflows that require temporary workarounds (like installing special system dependencies), document these with TODOs and create tickets to revisit them when the underlying issues are resolved. This helps manage technical debt in your CI/CD configurations.