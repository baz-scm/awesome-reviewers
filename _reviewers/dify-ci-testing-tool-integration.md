---
title: CI testing tool integration
description: When integrating new testing or analysis tools into CI pipelines, use
  graceful failure patterns during initial adoption phases to prevent breaking existing
  workflows. Add tools as development dependencies and allow them to fail without
  blocking builds using `|| true` until they are stable and properly configured.
repository: langgenius/dify
label: Testing
language: Yaml
comments_count: 2
repository_stars: 114231
---

When integrating new testing or analysis tools into CI pipelines, use graceful failure patterns during initial adoption phases to prevent breaking existing workflows. Add tools as development dependencies and allow them to fail without blocking builds using `|| true` until they are stable and properly configured.

This approach allows teams to experiment with new testing tools without disrupting the development workflow. Once the tools are properly configured and any initial issues are resolved, the `|| true` can be removed to enforce the checks.

Example implementation:
```yaml
- name: Run new analysis tool
  run: |
    cd api
    uv add --dev new-tool
    uv run new-tool check || true
```

This pattern is particularly useful when introducing type checkers, linters, or other code analysis tools that may initially produce many findings on existing codebases.