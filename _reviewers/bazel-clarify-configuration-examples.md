---
title: Clarify configuration examples
description: Configuration documentation should provide concrete, platform-specific
  examples rather than generic placeholders, and use precise terminology to avoid
  confusion. Generic paths like `/path/to/repository` leave developers uncertain about
  actual implementation.
repository: bazelbuild/bazel
label: Configurations
language: Markdown
comments_count: 3
repository_stars: 24489
---

Configuration documentation should provide concrete, platform-specific examples rather than generic placeholders, and use precise terminology to avoid confusion. Generic paths like `/path/to/repository` leave developers uncertain about actual implementation.

Replace generic placeholders with realistic examples that show the actual structure and format expected:

```
# Instead of generic:
common --registry="path/to/local/bcr/registry"

# Provide platform-specific examples:
# Windows:
common --registry="file:///C:/Users/johndoe/bazel-central-registry-main"
# Linux:
common --registry="file:////home/johndoe/bazel-central-registry-main"
```

Additionally, ensure configuration instructions are complete by:
- Explaining why certain configurations are needed
- Providing context for workarounds or special cases
- Using precise terminology (e.g., "Bazel modules" vs "Go modules")
- Including references to relevant documentation for complex scenarios

This prevents confusion and reduces back-and-forth questions about implementation details, making configuration setup more straightforward for developers.