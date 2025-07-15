---
title: Use environment flags consistently
description: Feature flags like `__DEV__` and `__COMPAT__` are critical configuration
  mechanisms that control environment-specific behavior. Always wrap development-only
  code (such as warnings and debug information) in `__DEV__` conditionals to ensure
  they don't ship to production builds. Remember that these flags are replaced at
  build time through tree-shaking, so...
repository: vuejs/core
label: Configurations
language: TypeScript
comments_count: 3
repository_stars: 50769
---

Feature flags like `__DEV__` and `__COMPAT__` are critical configuration mechanisms that control environment-specific behavior. Always wrap development-only code (such as warnings and debug information) in `__DEV__` conditionals to ensure they don't ship to production builds. Remember that these flags are replaced at build time through tree-shaking, so their proper usage directly impacts bundle size and performance.

```js
// Good: Warning only shown in development
if (__DEV__ && unexpectedCondition) {
  console.warn('This warning helps developers but is removed in production')
}

// Good: Feature flag affects code path selection
if (!(__COMPAT__ && compatFeature)) {
  // Modern implementation
} else {
  // Compatibility implementation
}

// Bad: Warning always included in production builds
if (unexpectedCondition) {
  console.warn('This warning will bloat production builds')
}
```

This practice ensures configuration is properly managed across different build environments, keeping production code lean while providing helpful development features.