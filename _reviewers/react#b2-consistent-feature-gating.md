---
title: Consistent Feature Gating
description: 'When adding or modifying behavior behind feature flags or __DEV__-like
  conditions, ensure the gating is correct, consistent, and maintainable.


  Apply these rules:'
repository: facebook/react#b2
label: Configurations
language: JavaScript
comments_count: 7
repository_stars: 251882
---

When adding or modifying behavior behind feature flags or __DEV__-like conditions, ensure the gating is correct, consistent, and maintainable.

Apply these rules:
1) Gate at the right boundary: guard the entire block (or all call sites), not individual statements, so code doesn’t call into flag-dependent functions when the feature is actually off.
2) Keep gating semantics understandable: prefer explicit, stable conditions (e.g., DEV-only vs “depends on DevTools installed”) to avoid confusing “works for some teammates” behavior.
3) Prefer implementation guards over entrypoint complexity: it’s acceptable to pass options/values through as long as the implementation already safely guards their usage.
4) Write gates in a consistent shape: use the flag as the outer condition, then handle any secondary checks inside (avoids scattered/implicit gating).
5) Rollout discipline: enable new flags widely first, keep the flag present until stabilization, and allow rapid disablement if it breaks.
6) Use the project’s flag gating mechanism in tests (e.g., gate('flag')) rather than importing feature-flag modules directly, so tests match the runtime wiring.

Example pattern:
```js
// Good: flag gates the whole behavior
if (enableFragmentRefsTextNodes) {
  if (child.tag === HostText) {
    // scroll logic
  }
}

// Good: async debug-only code runs only when the feature is enabled
if (__DEV__ && enableAsyncDebugInfo) {
  resolveDebugValue(debugValue);
}
```
