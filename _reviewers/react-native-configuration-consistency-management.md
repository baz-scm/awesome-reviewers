---
title: configuration consistency management
description: Maintain consistent configuration references across all code branches
  and document temporary configuration code for future cleanup. Configuration inconsistencies
  can lead to compilation errors and maintenance debt.
repository: facebook/react-native
label: Configurations
language: Java
comments_count: 2
repository_stars: 123178
---

Maintain consistent configuration references across all code branches and document temporary configuration code for future cleanup. Configuration inconsistencies can lead to compilation errors and maintenance debt.

When using feature flags or configuration classes, ensure the same class names and method signatures are used consistently across different branches or versions. For example, avoid mixing `ReactFeatureFlags.enableBridgelessArchitecture` and `ReactNativeFeatureFlags.enableBridgelessArchitecture()` in different parts of the codebase.

For temporary configuration code (such as version checks or compatibility shims), add clear comments indicating when the code should be removed:

```java
// TODO: Remove when minSdk is bumped to 26
int justificationMode = (Build.VERSION.SDK_INT < Build.VERSION_CODES.O) 
    ? 0 : Layout.JUSTIFICATION_MODE_NONE;
```

This practice prevents accumulation of obsolete configuration code and makes it easier to clean up when constraints change.