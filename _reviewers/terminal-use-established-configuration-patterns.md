---
title: Use established configuration patterns
description: When adding new configuration options or settings, leverage existing
  configuration frameworks and patterns rather than implementing custom solutions.
  This ensures consistency, reduces boilerplate code, and maintains alignment with
  established practices.
repository: microsoft/terminal
label: Configurations
language: Other
comments_count: 6
repository_stars: 99242
---

When adding new configuration options or settings, leverage existing configuration frameworks and patterns rather than implementing custom solutions. This ensures consistency, reduces boilerplate code, and maintains alignment with established practices.

For settings, use the appropriate macro systems:
```cpp
// Instead of manual implementation
bool UseMicaAlt() const;
bool _useMicaAlt = false;

// Use the established macro pattern
#define MTSM_GLOBAL_SETTINGS_FIELDS(X) \
    X(bool, UseMicaAlt, "useMicaAlt", false)
```

For configuration files, follow existing patterns in the codebase. When multiple variants are needed (like different Visual Studio editions), create separate configuration files following established naming conventions rather than trying to handle all cases in one file.

Avoid runtime configuration decisions that should be compile-time. Configuration values should not be exposed broadly with generic names, and branding-specific code should be compiled out rather than decided at runtime.

When adding new configuration options, ensure corresponding schema files and documentation are updated to maintain consistency across the system.