---
title: Balance CI/CD trade-offs
description: When configuring CI/CD pipelines, balance comprehensive coverage and
  security with practical constraints like resource usage, tool compatibility, and
  project context. Avoid blindly applying best practices without considering their
  impact on functionality and efficiency.
repository: langgenius/dify
label: CI/CD
language: Yaml
comments_count: 3
repository_stars: 114231
---

When configuring CI/CD pipelines, balance comprehensive coverage and security with practical constraints like resource usage, tool compatibility, and project context. Avoid blindly applying best practices without considering their impact on functionality and efficiency.

Consider these trade-offs:
- **Permissions**: Start with minimal permissions but adjust when tools require broader access to function correctly
- **Test matrices**: Include comprehensive version coverage when possible, but prioritize the most critical versions when resources are limited
- **Automation frequency**: Match update intervals to your project's actual needs rather than using default aggressive settings

Example from a GitHub workflow:
```yaml
strategy:
  matrix:
    python-version:
      - "3.12"  # Primary version for most users
      # - "3.11"  # Commented out to save CI resources
```

Document your reasoning when making these trade-offs so future maintainers understand the decisions and can revisit them as constraints change.