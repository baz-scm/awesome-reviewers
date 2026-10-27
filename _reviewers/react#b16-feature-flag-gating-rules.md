---
title: Feature flag gating rules
description: 'When adding/changing behavior behind feature flags, apply flags consistently
  and safely:


  - Gate the *entire* code path that depends on the flag (not just individual helpers).
  This prevents invalid calls when the flag isn’t enabled everywhere and improves
  DCE/readability.'
repository: facebook/react#b16
label: Configurations
language: JavaScript
comments_count: 7
repository_stars: 251891
---

When adding/changing behavior behind feature flags, apply flags consistently and safely:

- Gate the *entire* code path that depends on the flag (not just individual helpers). This prevents invalid calls when the flag isn’t enabled everywhere and improves DCE/readability.
- Use the standard flag gating helper (e.g. `gate('flagName')`) in tests and call sites instead of importing the feature-flag module directly.
- Follow the existing pattern for where to guard: typically keep entrypoints “thin” and implement guards in the shared implementation layer when other code already does so.
- Rollout/removal: keep flags present during rollout, enable broadly first (or widely enough for the target environments), and only remove after stability so you can quickly disable if OSS behavior regresses.
- Don’t prematurely remove flags from environments that currently don’t use the feature; keeping the wiring helps ensure safe future cleanup.

Example (gate the whole dependent block):
```js
import { gate } from './path/to/flag-gate';

function resolveDebugInfo(payload, ioInfo) {
  if (!gate('enableAsyncDebugInfo')) return;
  // Only call flag-dependent APIs when the flag is on
  resolveDebugValue(payload.moduleObject?.default);
  ioInfo.value.status = 'fulfilled';
  ioInfo.value.value = payload.moduleObject?.default;
}
```

Example (test gating):
```js
import { gate } from '../utils/flag-gate';

if (gate('enableTrustedTypesIntegration')) {
  expect(ttCall[2]).toBe(ttObject);
}
```

These practices reduce inconsistent behavior across environments, make rollouts safer, and keep flag usage maintainable over time.