---
title: Config gating discipline
description: 'When changing behavior behind feature flags, DEV/debug paths, or environment-specific
  config, apply a consistent gating + rollout approach:


  - **Gate the entire behavior block** (not just inner calls) so code that depends
  on a flag/DEV capability is never partially executed.'
repository: facebook/react#b5
label: Configurations
language: JavaScript
comments_count: 5
repository_stars: 251886
---

When changing behavior behind feature flags, DEV/debug paths, or environment-specific config, apply a consistent gating + rollout approach:

- **Gate the entire behavior block** (not just inner calls) so code that depends on a flag/DEV capability is never partially executed.
- **Scope semantic changes** to the exact stream/data context where they’re correct (don’t assume a transformation is universally safe).
- **Roll out flags safely in OSS** by enabling broadly first (or at least early) so you can quickly disable via the flag if issues appear; keep the flag until removal is truly safe.
- **Use the standard gating helper** (e.g. `gate('someFlag')`) in tests and configuration checks instead of importing feature-flag modules directly.

Example pattern (gate the whole block):

```js
// Instead of partially relying on internal guards,
// guard the whole debug/flag-dependent block.
if (__DEV__ && enableAsyncDebugInfo) {
  // debug/diagnostic work that must not run otherwise
  resolveDebugValue(...);
}
```

Adopting these rules prevents unintended side effects, improves DCE/readability, and makes rollouts/rollback predictable.