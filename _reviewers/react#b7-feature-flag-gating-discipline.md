---
title: Feature flag gating discipline
description: 'Adopt a consistent, rollout-safe approach to feature flags and dev/prod
  gating.


  **1) Rollout safety**

  - Keep the flag while migrating/cleaning up behavior.'
repository: facebook/react#b7
label: Configurations
language: JavaScript
comments_count: 9
repository_stars: 251888
---

Adopt a consistent, rollout-safe approach to feature flags and dev/prod gating.

**1) Rollout safety**
- Keep the flag while migrating/cleaning up behavior.
- When moving a flag from experimental/limited environments to broader use, **enable everywhere first**, then revert quickly if needed.

**2) Gate at the right scope**
- If code depends on a flag (or async debug support), **gate the entire block** that uses the capability (not just inner calls), to improve clarity and allow better dead-code elimination.
- Prefer **implementation-level guarding** when entrypoints already pass options through (i.e., don’t add extra entrypoint flags if the implementation already contains the correct guards).

**3) Avoid redundant or inconsistent guards**
- Don’t add `__DEV__` checks in places that are already dev-only by construction.
- Use consistent semantics: if behavior can depend on DevTools presence, ensure that’s intentional and not surprising compared to always-enabled `<Profiler>`-style behavior.

**4) Testing**
- In tests, follow the existing flag-gating utilities (e.g., use `gate('flagName')`) rather than importing the shared runtime flag modules.

**Example pattern**
```js
// Good: gate the whole block that uses capability
if (enableAsyncDebugInfo) {
  // Entire debug-info path is safe to run here
  resolveDebugValue(debugValue);
  ioInfo.value.status = 'fulfilled';
  ioInfo.value.value = debugValue;
}

// Good: minimal, direct gating
if (enableFragmentRefsTextNodes) {
  if (child.tag === HostText) {
    // ...
  }
}

// Good: avoid redundant dev checks
// (only add __DEV__ if this code path can run outside dev)
```

Applying these rules will make flag behavior safer to ship, easier to understand, and less error-prone across environments.