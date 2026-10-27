---
title: Consistent Feature Flag Gating
description: When adding or updating configuration/feature-flag-driven logic (especially
  debug/profiler behavior), ensure gating is consistent, complete, and uses the team’s
  standard flag access.
repository: facebook/react#b13
label: Configurations
language: JavaScript
comments_count: 9
repository_stars: 251893
---

When adding or updating configuration/feature-flag-driven logic (especially debug/profiler behavior), ensure gating is consistent, complete, and uses the team’s standard flag access.

Apply these rules:
1) Gate whole blocks, not just callees
- If a helper/function is only valid when a specific enable flag or __DEV__ is true, wrap the entire block so it’s clearly unreachable otherwise and is easier for DCE/minification.

```js
// Good: gate the whole block
if (enableAsyncDebugInfo) {
  resolveDebugValue(debugValue);
  ioInfo.value.status = 'fulfilled';
  ioInfo.value.value = debugValue;
}

// Avoid: only gating inside while leaving the block ungated
// (can confuse DCE/readers and may violate invariants)
```

2) Keep call sites consistently dev/debug guarded
- If one call site is guarded and others aren’t, align them (either guard all call sites or prove the invariants with equivalent gating).

3) Prefer the standard flag access mechanism
- In tests/clients, use the established gating helper (e.g., `gate('someFlag')`) instead of importing feature-flag modules directly.

```js
// Good in tests
if (gate('enableTrustedTypesIntegration')) {
  // ...
}
```

4) Choose a single location for gating: entrypoint vs implementation
- Follow existing patterns: commonly, keep entrypoints thin and rely on implementation-side guards, rather than duplicating gating in multiple layers.

5) Roll out safely before removal
- Before removing a flag, enable it broadly (“everywhere first”) so you can still disable quickly if OSS/real environments break; also keep it present/enabled in non-primary environments to avoid later uncertainty about safe removal.

Outcome: fewer confusing environment-dependent behaviors, cleaner DCE/readability, and safer feature-flag lifecycle management.