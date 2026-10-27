---
title: Consistent Feature Gating
description: 'When adding/changing feature-flagged or environment-specific behavior,
  use a consistent gating strategy:


  - **Rollout safely:** if a flag exists because OSS differs from internal, **enable
  it broadly first** (everywhere), and keep the flag as a **fast rollback switch**
  rather than removing it immediately.'
repository: facebook/react#b14
label: Configurations
language: JavaScript
comments_count: 6
repository_stars: 251893
---

When adding/changing feature-flagged or environment-specific behavior, use a consistent gating strategy:

- **Rollout safely:** if a flag exists because OSS differs from internal, **enable it broadly first** (everywhere), and keep the flag as a **fast rollback switch** rather than removing it immediately.
- **Gate the right way:** use the project’s standard gating helper (e.g., `gate('flagName')`) instead of importing feature-flag modules directly in call sites/tests.
- **Gate consistently in the right layer:** prefer **implementation-level guards** for option/behavior differences (especially when implementations already handle `__DEV__`/flag logic), rather than sprinkling entrypoint checks that can drift.
- **Dev/debug correctness:** if behavior is debug-only, **wrap the entire behavior block** with the appropriate dev/debug guard—don’t rely on partial/inner checks that are easy to miss.
- **Avoid redundant dev-only paths:** ensure code that is not reachable in dev is not doing extra dev-only work.

Example pattern (implementation-level + full block dev gate):
```js
import {gate} from 'shared/gate';

const enableFoo = gate('enableFoo');

export function maybeDoFoo(options) {
  if (!enableFoo) return;

  // If this is debug-only, guard the whole block
  if (__DEV__) {
    // debug/log/extra work
    debugDoFoo(options);
  }

  doFoo(options);
}
```