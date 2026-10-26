---
title: Feature-flag rollout discipline
description: 'When introducing or changing feature-flagged behavior, follow a consistent
  rollout + gating pattern:


  1) Roll out in safe phases

  - Enable the flag “everywhere first” (or broadly in the relevant fleet) before any
  removal.'
repository: facebook/react#b3
label: Configurations
language: JavaScript
comments_count: 6
repository_stars: 251883
---

When introducing or changing feature-flagged behavior, follow a consistent rollout + gating pattern:

1) Roll out in safe phases
- Enable the flag “everywhere first” (or broadly in the relevant fleet) before any removal.
- Keep the flag during the rollout window so it can be disabled quickly if OSS/other environments break.

2) Gate entire blocks consistently
- If a helper is only valid when a flag is enabled (or when debugging/profiling is supported), guard the whole call/instrumentation block—not just internal calls. This improves readability and helps dead-code elimination.

3) Use the proper gating API
- In tests and other non-production entrypoints, use the same gating mechanism the codebase expects (e.g., `gate('flag')`) rather than importing the feature-flag module directly.

4) Guard in the implementation, not the entrypoint (when that’s the existing convention)
- Prefer guarding the behavior inside the implementation layer so callers/entrypoints don’t need to duplicate feature-flag logic.

Example pattern (whole-block gating + consistent gate usage):
```js
// Example: whole-block guard + safe instrumentation
import {gate} from './gate';

const enableMyFeature = gate('enableMyFeature');

function maybeInstrument(payload) {
  if (!enableMyFeature) return;

  // Safe: everything in here assumes the feature is enabled
  startInstrumentation(payload);
  resolveDebugValue(payload);
}
```

Apply this standard whenever you see new flags, toggled defaults, or debug/profiling instrumentation behind flags—especially where partial gating could cause confusing behavior across environments.