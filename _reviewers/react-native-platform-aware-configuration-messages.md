---
title: platform-aware configuration messages
description: Configuration-related error messages, troubleshooting guidance, and feature
  flags should be accurate and account for platform-specific differences. When providing
  configuration instructions or enabling features conditionally, ensure the guidance
  reflects the actual capabilities and limitations of each target platform.
repository: facebook/react-native
label: Configurations
language: C++
comments_count: 2
repository_stars: 123178
---

Configuration-related error messages, troubleshooting guidance, and feature flags should be accurate and account for platform-specific differences. When providing configuration instructions or enabling features conditionally, ensure the guidance reflects the actual capabilities and limitations of each target platform.

For error messages, provide clear, actionable troubleshooting steps that are relevant to the user's environment:

```cpp
// Good: Platform-aware error message with specific guidance
throw std::runtime_error(folly::to<std::string>(
    "Unable to load script.\n\n"
    "Make sure you're running Metro or that your "
    "bundle '", assetName, "' is packaged correctly for release.\n\n"
    "The device must be on the same Wi-Fi network as your laptop to connect to Metro.\n\n"
    "To use USB instead, shake the device to open the Dev Menu and set "
    "the bundler location to \"localhost:8081\" and run:\n"
    "  adb reverse tcp:8081 tcp:8081"));
```

For feature flags, consider platform capabilities when enabling conditional compilation:

```cpp
#if AUTOLINKING_AVAILABLE
// Feature only enabled where actually supported
// Note: Android can't disable new arch at runtime unlike iOS
#endif
```

This ensures users receive relevant guidance and prevents configuration mismatches that could lead to runtime failures or unexpected behavior across different platforms.