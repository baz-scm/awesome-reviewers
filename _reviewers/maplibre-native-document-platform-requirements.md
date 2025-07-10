---
title: Document platform requirements
description: 'When setting or changing minimum platform version requirements, always
  document the specific technical reasons for these decisions. Include:


  1. Features or APIs that necessitate the change (e.g., std::filesystem requiring
  macOS 10.15+)'
repository: maplibre/maplibre-native
label: Configurations
language: Other
comments_count: 4
repository_stars: 1411
---

When setting or changing minimum platform version requirements, always document the specific technical reasons for these decisions. Include:

1. Features or APIs that necessitate the change (e.g., std::filesystem requiring macOS 10.15+)
2. Impact analysis on backward compatibility
3. Market considerations (e.g., iOS version distribution)

For libraries, consider using conditional compilation to support optional features that require newer platform versions while maintaining core functionality for older versions:

```cpp
// Example showing conditional use of std::filesystem
#if defined(__APPLE__)
  #include <TargetConditionals.h>
  #if TARGET_OS_MAC
    #if MAC_OS_X_VERSION_MIN_REQUIRED >= MAC_OS_X_VERSION_10_15
      // Use std::filesystem
      #include <filesystem>
      namespace fs = std::filesystem;
    #else
      // Use alternative implementation
      #include "custom_filesystem.hpp"
      namespace fs = custom_filesystem;
    #endif
  #endif
#endif

// Similarly for iOS:
#if defined(__APPLE__) && TARGET_OS_IOS
  #if __IPHONE_OS_VERSION_MIN_REQUIRED >= __IPHONE_13_0
    // Use iOS 13+ features
  #else
    // Fallback implementation
  #endif
#endif
```

Always validate platform-specific dependencies against your minimum version requirements. When library dependencies change (e.g., GLES versions), ensure compatibility with your stated platform minimums to avoid runtime failures.