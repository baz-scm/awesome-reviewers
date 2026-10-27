---
title: Consistent feature flags
description: 'When adding or changing feature-flagged behavior, apply a consistent
  configuration/flag policy across OSS and renderers:


  - **Enable widely first for safe rollback:** if a change wasn’t previously on for
  OSS, turn the flag on everywhere before removal so you can still disable quickly
  if it breaks.'
repository: facebook/react#b8
label: Configurations
language: JavaScript
comments_count: 5
repository_stars: 251889
---

When adding or changing feature-flagged behavior, apply a consistent configuration/flag policy across OSS and renderers:

- **Enable widely first for safe rollback:** if a change wasn’t previously on for OSS, turn the flag on everywhere before removal so you can still disable quickly if it breaks.
- **Keep flag definitions consistent across environments:** don’t leave flags arbitrarily “off” in platforms/targets (e.g., native) even if the code path seems unused—this prevents later rollout/removal friction and ambiguity.
- **Use the project’s standard flag gating mechanism:** prefer the common `gate('flag')` pattern instead of importing feature-flag modules directly.
- **Gate the entire affected block:** ensure the flag (or `__DEV__` where appropriate) wraps all code that depends on the flag, improving readability and enabling better dead-code elimination.

Example pattern:
```js
import {gate} from 'shared/ReactFeatureFlags';

export function maybeDoThing() {
  if (!gate('enableSomeFeature')) return;

  // Entire block is gated so it only runs when the flag is truly enabled.
  doThing();
}
```

Apply this to both production features and debug-only functionality to avoid environment-specific surprises and to make future flag removal straightforward.