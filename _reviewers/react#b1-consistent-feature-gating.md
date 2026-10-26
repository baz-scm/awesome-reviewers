---
title: Consistent Feature Gating
description: 'When introducing or changing feature-flagged, dev-only, debug, or profiling
  behavior:


  1) Roll out safely: enable the new flag broadly first (even if it’s off in open
  source), so it can be disabled quickly if it breaks. Remove or narrow the flag only
  after proving stability.'
repository: facebook/react#b1
label: Configurations
language: JavaScript
comments_count: 7
repository_stars: 251878
---

When introducing or changing feature-flagged, dev-only, debug, or profiling behavior:

1) Roll out safely: enable the new flag broadly first (even if it’s off in open source), so it can be disabled quickly if it breaks. Remove or narrow the flag only after proving stability.

2) Gate at the point of consumption: implement gating inside the code that uses the option/feature (entrypoints shouldn’t rely on callers to gate). Match the existing pattern for dev-only options.

3) Gate whole blocks, not just internal calls: if a block is only valid when a flag is enabled, guard the entire block for correctness, readability, and better dead-code elimination.

4) Use the team’s standard gating helper in tests: prefer the established `gate('flag')` mechanism over importing the feature-flag module directly.

5) Avoid redundant/misleading dev assumptions: only add `__DEV__` code where it’s actually reachable in dev builds.

Example pattern:

```js
// Good: gate the whole instrumentation block (not just one function call)
if (__DEV__ || (enableProfilerTimer && isDevToolsPresent)) {
  // collect timings / debug info
}

// Good: gate debug value resolution with the feature flag
if (enableAsyncDebugInfo) {
  const debugValue = moduleObject == null ? undefined : moduleObject.default;
  resolveDebugValue(debugValue);
  ioInfo.value.status = 'fulfilled';
  ioInfo.value.value = debugValue;
}
```

Apply this consistently to prevent accidental dev/profiling/debug execution, keep behavior predictable across environments, and ensure rollbacks remain possible.