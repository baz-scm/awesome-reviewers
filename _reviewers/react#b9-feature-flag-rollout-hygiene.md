---
title: Feature flag rollout hygiene
description: When introducing or changing feature flags/config-driven behavior, ensure
  rollout safety and consistent gating across renderers, platforms, dev/prod builds,
  and tests.
repository: facebook/react#b9
label: Configurations
language: JavaScript
comments_count: 6
repository_stars: 251891
---

When introducing or changing feature flags/config-driven behavior, ensure rollout safety and consistent gating across renderers, platforms, dev/prod builds, and tests.

**Rules**
1. **Roll out before removing:** If a flag change is needed for OSS/non-OSS parity, enable the flag broadly first (everywhere), then remove only after stability.
2. **Keep flags defined in all platform forks:** Even if a platform doesn’t use the codepath today, leaving the flag exported prevents later removal/cleanup from becoming blocked or confusing.
3. **Gate at the block level (not just inside):** If a flag controls whether a helper/function is legal/callable, gate the entire block that would call it. This prevents accidental invalid calls and improves DCE/readability.
4. **Use standard gating in tests:** Prefer the existing test gating helper (e.g. `gate('flag')`) rather than importing feature-flag modules directly.
5. **Keep gating style consistent:** Prefer simple, outer `if (enableFlag) { ... }` structure so reviewers can quickly verify all related logic is consistently controlled.

**Example pattern**
```js
// Production/build gating (block-level)
if (enableAsyncDebugInfo) {
  // Only call helpers that require enableAsyncDebugInfo
  resolveDebugValue(debugValue);
  ioInfo.value.status = 'fulfilled';
}

// Test gating (use helper)
gate('enableTrustedTypesIntegration', () => {
  expect(setAttributeCalls[0][2]).toBe(ttObject1);
});

// Consistent flag structure
if (enableFragmentRefsTextNodes) {
  if (child.tag === HostText) {
    // ...
  }
}
```

Applying these practices reduces rollout risk, avoids dev/prod mismatch, and keeps flags maintainable across forks and tests.