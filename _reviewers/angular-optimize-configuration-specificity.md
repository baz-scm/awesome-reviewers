---
title: Optimize configuration specificity
description: Ensure configuration files use precise patterns and avoid redundant dependencies.
  Configuration specifications should be as specific as necessary to match their intended
  purpose, and unnecessary or duplicate entries should be removed to maintain clean,
  efficient configurations.
repository: angular/angular
label: Configurations
language: Other
comments_count: 2
repository_stars: 98611
---

Ensure configuration files use precise patterns and avoid redundant dependencies. Configuration specifications should be as specific as necessary to match their intended purpose, and unnecessary or duplicate entries should be removed to maintain clean, efficient configurations.

When defining file patterns in build configurations, use specific glob patterns that match exactly what you need rather than overly broad selectors. For test configurations, explicitly target test files:

```bazel
# Instead of capturing all TypeScript files
srcs = glob(["**/*.ts"]),

# Be specific about test files
srcs = glob(["**/*.spec.ts"]),
```

Similarly, avoid specifying redundant dependencies when they are already provided by existing toolchain versions. Review dependency declarations to ensure each entry serves a unique purpose and remove any that are automatically included by other dependencies.