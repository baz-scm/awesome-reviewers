---
title: Consistent Feature Flag Gating
description: 'When adding or changing feature/config-flag behavior, make gating explicit,
  consistent, and rollout-friendly across environments.


  Apply these rules:

  1) Gate the *entire* behavior block when it depends on a specific flag/DEV capability
  (not just inner calls). This prevents accidental execution paths, improves DCE,
  and clarifies intent.'
repository: facebook/react#b6
label: Configurations
language: JavaScript
comments_count: 10
repository_stars: 251888
---

When adding or changing feature/config-flag behavior, make gating explicit, consistent, and rollout-friendly across environments.

Apply these rules:
1) Gate the *entire* behavior block when it depends on a specific flag/DEV capability (not just inner calls). This prevents accidental execution paths, improves DCE, and clarifies intent.
2) Use the standard flag gate helper (e.g., `gate('flag')`) in tests and similar contexts—avoid importing feature-flag modules directly.
3) Prefer a clear outer guard pattern: `if (flag) { ... }` rather than relying on deeper checks.
4) Roll out new flags by enabling broadly first (including non-OSS equivalents where applicable) and keep the flag present so it can be disabled quickly if issues arise.
5) Define/keep flags consistently across platforms/targets even if the renderer/entrypoint isn’t currently used, to avoid later removal uncertainty.
6) Ensure user-visible profiling/debug behavior doesn’t unexpectedly differ only because an unrelated environment happened to be installed.

Example (gate whole block):
```js
// Wrong: calling into flag-only helpers without guarding the entire block
function doDebugWork() {
  // resolveDebugValue() is only valid when enableAsyncDebugInfo is enabled
  resolveDebugValue();
}

// Right: guard the whole block (and match DEV semantics where needed)
function doDebugWork() {
  if (__DEV__ && enableAsyncDebugInfo) {
    const debugValue = moduleObject == null ? undefined : moduleObject.default;
    resolveDebugValue(debugValue);
  }
}
```

Example (test gating via helper):
```js
describe('Trusted Types integration', () => {
  it('does not stringify', () => {
    if (gate('enableTrustedTypesIntegration')) {
      expect(value).toBe(ttObject);
    }
  });
});
```