---
title: Cross-platform CI validation
description: 'Always verify that code changes work across all CI platforms before
  submitting. When addressing a CI issue for one platform, ensure your fix doesn''t
  break other environments. Common cross-platform CI issues include:'
repository: maplibre/maplibre-native
label: CI/CD
language: Other
comments_count: 3
repository_stars: 1411
---

Always verify that code changes work across all CI platforms before submitting. When addressing a CI issue for one platform, ensure your fix doesn't break other environments. Common cross-platform CI issues include:

1. **Missing includes:** Add all necessary includes required by different compilers/platforms.
```cpp
// Add includes needed by all platforms, even if your primary dev environment doesn't require them
#include <array>  // Required by Node.js CI
```

2. **Unused code:** Either remove unused code, move it to an appropriate implementation file, or conditionally compile it for specific platforms.
```cpp
#ifdef PLATFORM_DARWIN
// Darwin-specific implementation
#endif
```

3. **Build configuration:** Make build parameters configurable rather than hardcoded.
```
// In config.bzl or equivalent
BUILD_MODE = "bazel"  // Can be configured per developer or environment
```

When CI fails on any platform, investigate thoroughly and implement a solution that works across all environments. This prevents development bottlenecks from recurring platform-specific issues and ensures consistent behavior across the entire build pipeline.