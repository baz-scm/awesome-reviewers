---
title: consistent naming conventions
description: 'Follow the project''s established naming conventions consistently across
  all code. Use camelCase for variables, functions, and parameters, avoiding Hungarian
  notation and snake_case. Apply type-specific prefixes: classes should have a ''C''
  prefix (e.g., `CXCBConnection`), enums should have an ''e'' prefix (e.g., `eAutoDirs`),
  and enum values should be in CAPS...'
repository: hyprwm/Hyprland
label: Naming Conventions
language: Other
comments_count: 6
repository_stars: 28863
---

Follow the project's established naming conventions consistently across all code. Use camelCase for variables, functions, and parameters, avoiding Hungarian notation and snake_case. Apply type-specific prefixes: classes should have a 'C' prefix (e.g., `CXCBConnection`), enums should have an 'e' prefix (e.g., `eAutoDirs`), and enum values should be in CAPS with descriptive prefixes (e.g., `DIR_AUTO_UP`). When possible, wrap standalone functions in appropriate namespaces rather than leaving them in global scope.

Example transformations:
```cpp
// Before
class XCBConnection { };           // Missing C prefix
enum class AutoDirs { auto_up };   // Missing e prefix, snake_case
bool m_benabled;                   // Hungarian notation
void some_function();              // snake_case

// After  
class CXCBConnection { };          // C prefix for classes
enum class eAutoDirs { DIR_AUTO_UP }; // e prefix, CAPS enum values
bool m_enabled;                    // No Hungarian notation
void someFunction();               // camelCase
```

This ensures code readability and maintains consistency with the existing codebase, making it easier for developers to understand type information at a glance and follow established patterns.