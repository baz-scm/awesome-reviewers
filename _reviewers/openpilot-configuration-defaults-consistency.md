---
title: Configuration defaults consistency
description: Ensure configuration parameters have appropriate default values, consistent
  naming conventions, and centralized default management. When adding new configuration
  keys, consider security implications for defaults (e.g., audio recording should
  default to off), maintain consistent naming patterns with existing keys, and centralize
  default values in the...
repository: commaai/openpilot
label: Configurations
language: Other
comments_count: 3
repository_stars: 58214
---

Ensure configuration parameters have appropriate default values, consistent naming conventions, and centralized default management. When adding new configuration keys, consider security implications for defaults (e.g., audio recording should default to off), maintain consistent naming patterns with existing keys, and centralize default values in the configuration structure rather than scattered throughout the codebase.

Example of good practice:
```cpp
inline static std::unordered_map<std::string, ParamKeyAttributes> keys = {
    {"AdbEnabled", {PERSISTENT}},  // Consistent with SshEnabled naming
    {"RecordAudioFeedback", {PERSISTENT, BOOL, "0"}},  // Default off for privacy
    // Centralized defaults as third parameter
};
```

This approach improves maintainability, reduces configuration errors, and ensures security-conscious defaults for sensitive features.