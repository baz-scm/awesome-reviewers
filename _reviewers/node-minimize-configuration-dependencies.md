---
title: Minimize configuration dependencies
description: Keep configuration dependencies minimal and platform-aware. Avoid including
  unnecessary configuration files or external tools that can introduce unpredictable
  behaviors or unrelated settings. For platform-specific code, use conditional compilation
  to ensure that components are only built and executed in relevant environments.
repository: nodejs/node
label: Configurations
language: Other
comments_count: 5
repository_stars: 112178
---

Keep configuration dependencies minimal and platform-aware. Avoid including unnecessary configuration files or external tools that can introduce unpredictable behaviors or unrelated settings. For platform-specific code, use conditional compilation to ensure that components are only built and executed in relevant environments.

When working with build configurations:
1. Only include necessary configuration files that are directly relevant to the component being built
2. Use conditional compilation for platform-specific code
3. Minimize dependencies on external tools with behaviors that may change unexpectedly

Example of good practice for platform-specific code:

```cpp
// For header files
#ifndef SRC_NODE_PLATFORM_FEATURE_H_
#define SRC_NODE_PLATFORM_FEATURE_H_

#ifdef _WIN32
// Windows-specific declarations
#endif

// Cross-platform declarations

#endif  // SRC_NODE_PLATFORM_FEATURE_H_

// For implementation files
#ifdef _WIN32
// Windows-specific implementation
#endif
```

Example of good configuration file practice:
```
// Only include what you need
'includes': ['toolchain.gypi'],  // Correct if only toolchain config is needed

// Avoid unnecessary inclusions
'includes': ['toolchain.gypi', 'features.gypi'],  // Incorrect if features.gypi adds unneeded complexity
```