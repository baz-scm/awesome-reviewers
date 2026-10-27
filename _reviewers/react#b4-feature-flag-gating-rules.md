---
title: Feature flag gating rules
description: 'When adding or modifying feature-flagged/config-dependent behavior,
  follow a consistent gating and rollout pattern:


  - **Gate at the top of the block**: Wrap the whole code path in the relevant condition
  (feature flag and/or `__DEV__`) rather than relying only on inner checks. This improves
  readability and enables better dead-code elimination.'
repository: facebook/react#b4
label: Configurations
language: JavaScript
comments_count: 7
repository_stars: 251885
---

When adding or modifying feature-flagged/config-dependent behavior, follow a consistent gating and rollout pattern:

- **Gate at the top of the block**: Wrap the whole code path in the relevant condition (feature flag and/or `__DEV__`) rather than relying only on inner checks. This improves readability and enables better dead-code elimination.
- **Use the standard gating mechanism**: Prefer the repo’s approved `gate('flag')`/feature-gating API in places like tests instead of importing feature-flag modules directly.
- **Roll out safely**: If a flag isn’t enabled in OSS, first **enable it everywhere** (for the intended rollout window) and keep the flag present so it can be quickly disabled if something breaks; only remove after it’s proven stable.
- **Keep config/environment boundaries explicit**: If browser vs server configs require different implementations, split into separate entrypoints rather than shipping a shared one.

Example (pattern):
```js
// Top-level gating for readability + DCE
if (__DEV__ && enableAsyncDebugInfo) {
  // instrumentation / debug-only logic here
}

// Tests: gate via the standard mechanism (not direct imports)
if (gate('enableTrustedTypesIntegration')) {
  // assertions / expected behavior
}
```

Applying these rules will make configuration changes safer to roll out, easier to reason about, and less likely to accidentally run in the wrong environment.