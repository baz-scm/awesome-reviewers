---
title: Optimize CI configurations
description: When designing CI/CD workflows, prioritize both resource efficiency and
  clear documentation. Incorporate dynamic configuration where beneficial, but avoid
  creating separate jobs for simple tasks that can be handled within existing steps.
  Ensure all comments and configurations accurately reflect version requirements across
  all supported branches,...
repository: apache/airflow
label: CI/CD
language: Yaml
comments_count: 2
repository_stars: 40858
---

When designing CI/CD workflows, prioritize both resource efficiency and clear documentation. Incorporate dynamic configuration where beneficial, but avoid creating separate jobs for simple tasks that can be handled within existing steps. Ensure all comments and configurations accurately reflect version requirements across all supported branches, particularly when backporting is necessary.

Example for efficient runner configuration:
```yaml
build-info:
  name: "Build info"
  runs-on: >-
    # Dynamic runner configuration that doesn't require a separate job
    # Explanation of why this approach was chosen and what it accomplishes
```

Maintain clear documentation about version requirements in configuration files, especially when different branches have different version support. When a comment mentions supported versions (like Python versions), ensure it's accurate and consider adding notes about special cases like backporting requirements.