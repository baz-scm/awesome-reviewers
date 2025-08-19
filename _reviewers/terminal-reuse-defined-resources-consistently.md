---
title: Reuse defined resources consistently
description: Always reuse existing defined constants, resources, and reusable components
  instead of duplicating values or creating redundant implementations. This improves
  maintainability, ensures consistency across the codebase, and reduces the risk of
  introducing inconsistencies when values need to be updated.
repository: microsoft/terminal
label: Code Style
language: Other
comments_count: 4
repository_stars: 99242
---

Always reuse existing defined constants, resources, and reusable components instead of duplicating values or creating redundant implementations. This improves maintainability, ensures consistency across the codebase, and reduces the risk of introducing inconsistencies when values need to be updated.

Key practices:
- Reference existing resource definitions like `{StaticResource StandardControlMaxWidth}` instead of hardcoding values like "1000"
- Consolidate duplicate styles that serve the same purpose (e.g., merge `SettingsStackStyle` and `PivotStackStyle` if they're identical)
- Move reusable utility functions to shared locations like converters for project-wide access
- Avoid introducing duplicate constants across compilation units by moving them into appropriate scopes

Example of good practice:
```xml
<!-- Good: Reuse existing resource -->
<muxc:BreadcrumbBar MaxWidth="{StaticResource StandardControlMaxWidth}" />

<!-- Bad: Hardcode the same value -->
<muxc:BreadcrumbBar MaxWidth="1000" />
```

Example for C++ constants:
```cpp
// Good: Move constant into function scope to avoid duplication
uint64_t rapidhash_withSeed(const void* key, size_t len, uint64_t seed) {
    static const uint64_t rapid_secret[3] = { /* values */ };
    // use rapid_secret here
}

// Bad: Global constant duplicated in every compilation unit
static const uint64_t rapid_secret[3] = { /* values */ };
```

This approach reduces maintenance burden and ensures consistent behavior across the application.