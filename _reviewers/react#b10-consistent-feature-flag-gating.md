---
title: Consistent Feature Flag Gating
description: 'When adding or changing behavior behind feature flags, make the gating
  consistent, predictable, and rollback-friendly.


  Rules:

  - Rollouts: introduce/keep the flag and prefer enabling “everywhere” first, so you
  can quickly disable if OSS/users break.'
repository: facebook/react#b10
label: Configurations
language: JavaScript
comments_count: 5
repository_stars: 251894
---

When adding or changing behavior behind feature flags, make the gating consistent, predictable, and rollback-friendly.

Rules:
- Rollouts: introduce/keep the flag and prefer enabling “everywhere” first, so you can quickly disable if OSS/users break.
- Full-block gating: if a feature flag controls access to helpers/data, gate the entire block that uses them (not just inner call paths) to improve readability and enable dead-code elimination.
- Standard gating location: follow existing conventions—prefer gating inside the implementation (not in entrypoint glue) unless the codebase already does entrypoint gating.
- Standard access: in tests and call sites, use the team’s approved flag accessor (e.g., `gate('flag')`) rather than importing the flag module.

Example pattern:
```js
import { gate } from './featureFlags';

export function maybeDoNewThing(opts) {
  if (!gate('enableNewThing')) return;

  // Gate the whole block that depends on the feature.
  return doNewThing(opts);
}
```

If you need environment/dev behavior too, combine it explicitly (e.g., `__DEV__ || gate('...')`) so it’s clear when profiling/debugging is expected to work and avoid surprises from external state.