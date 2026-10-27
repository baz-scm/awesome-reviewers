---
title: Feature flag rollout and gating
description: 'When adding or changing feature flags/config options, follow a consistent
  rollout + gating approach:


  - **Keep the flag defined everywhere** (including platforms/renderers where it’s
  currently disabled) so removal/migration isn’t blocked later.'
repository: facebook/react#b12
label: Configurations
language: JavaScript
comments_count: 7
repository_stars: 251896
---

When adding or changing feature flags/config options, follow a consistent rollout + gating approach:

- **Keep the flag defined everywhere** (including platforms/renderers where it’s currently disabled) so removal/migration isn’t blocked later.
- **Roll out by enabling broadly first**, then rely on the flag to quickly disable/revert if anything breaks (especially for OSS parity).
- **Apply guards in the implementation, not just the entrypoints**. Pass options through as needed, but ensure the behavior is actually gated where it’s consumed.
- **Use the standard flag access mechanism** in tests/consumers (e.g. `gate('flagName')`), rather than importing the feature-flag module directly.
- **Ensure dev/debug-only behavior is gated consistently** around the behavior itself (not partially), so instrumentation/debug transfer/profiler logic only runs when appropriate.

Example pattern (test usage):
```js
import {gate} from 'path/to/gate';

// Instead of importing the flag module directly:
expect(gate('enableTrustedTypesIntegration')).toBe(true);
```

Example pattern (implementation-level gating):
```js
function someDebugBehavior(options) {
  if (!enableSomeFlag || !options) return;
  // ...debug behavior...
}
```