---
title: evaluate dependency API compatibility
description: Before adding or updating dependencies, thoroughly evaluate API compatibility
  and understand the implications of using forks versus upstream versions. This prevents
  recurring dependency issues and ensures long-term maintainability.
repository: docker/compose
label: API
language: Other
comments_count: 2
repository_stars: 35858
---

Before adding or updating dependencies, thoroughly evaluate API compatibility and understand the implications of using forks versus upstream versions. This prevents recurring dependency issues and ensures long-term maintainability.

Key evaluation steps:
1. **Identify API differences**: Document what patches or changes exist in forked dependencies compared to upstream
2. **Assess upstream status**: Check if fork-specific changes have been upstreamed or rejected, and understand the reasoning
3. **Avoid duplicate dependencies**: Prevent having multiple forks of the same dependency in your dependency tree
4. **Plan migration path**: For necessary forks, establish a clear path to contribute changes upstream or migrate to upstream versions

Example from dependency analysis:
```go
// Before adding:
require github.com/tilt-dev/fsnotify v1.4.8-0.20220602155310-fff9c274a375

// Evaluate: What API differences exist?
// - SetRecursive method not in upstream
// - Windows-specific patches upstreamed but not released
// - Consider pinning to upstream commit hash as interim solution
```

This approach helps avoid situations where dependencies cause recurring problems or create maintenance burdens due to API incompatibilities.