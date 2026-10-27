---
title: Use Named Transition Types
description: 'When the code uses shared identifier strings (e.g., UI transition “types”),
  don’t inline raw literals. Instead:

  1) Use semantically descriptive names that reflect the action/meaning (avoid generic
  names like just `tab`).'
repository: facebook/react#b13
label: Naming Conventions
language: TSX
comments_count: 2
repository_stars: 251893
---

When the code uses shared identifier strings (e.g., UI transition “types”), don’t inline raw literals. Instead:
1) Use semantically descriptive names that reflect the action/meaning (avoid generic names like just `tab`).
2) Centralize them in a shared module so all usages match.
3) Ensure uniqueness to prevent collisions with future unrelated transitions (use a prefix/scope pattern).

Example:

```ts
// apps/playground/lib/transitionTypes.ts
export const transitionTypes = {
  TOGGLE_TAB: 'playground:toggle-tab',
  CONFIG_PANEL: 'playground:config-panel',
} as const;

export type TransitionType =
  (typeof transitionTypes)[keyof typeof transitionTypes];
```

```ts
import {transitionTypes} from 'apps/playground/lib/transitionTypes';

startTransition(() => {
  addTransitionType(transitionTypes.TOGGLE_TAB);
});
```