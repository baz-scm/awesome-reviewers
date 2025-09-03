---
title: precise build targeting
description: Build targets should use specific file patterns rather than broad globs
  to improve build performance, clarity, and maintainability. Avoid capturing unnecessary
  files that can lead to build system constraints and complexity.
repository: angular/angular
label: CI/CD
language: Other
comments_count: 3
repository_stars: 98611
---

Build targets should use specific file patterns rather than broad globs to improve build performance, clarity, and maintainability. Avoid capturing unnecessary files that can lead to build system constraints and complexity.

When defining build targets, be explicit about which files are actually needed rather than using overly broad patterns like `glob(["**/*.ts"])`. This prevents unintended dependencies, reduces build times, and makes the build configuration more understandable.

Example of improvement:
```bazel
# Instead of broad globbing
srcs = glob(["**/*.ts"]),

# Use specific patterns
srcs = glob(["*.spec.ts"]),
```

Additionally, consider organizing BUILD files closer to the source files they target. If a build target primarily globs files from a specific subdirectory, it may be better to create a BUILD file in that subdirectory rather than managing it from a parent directory. This approach reduces complexity and makes the build structure more intuitive.