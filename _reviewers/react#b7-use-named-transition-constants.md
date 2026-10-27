---
title: Use named transition constants
description: For cross-component transition identifiers, avoid inline string literals.
  Use a shared, centrally exported constant for each transition type, and choose a
  semantic, action-descriptive name that’s unlikely to collide with future unrelated
  transitions.
repository: facebook/react#b7
label: Naming Conventions
language: TSX
comments_count: 2
repository_stars: 251888
---

For cross-component transition identifiers, avoid inline string literals. Use a shared, centrally exported constant for each transition type, and choose a semantic, action-descriptive name that’s unlikely to collide with future unrelated transitions.

Apply it like this:

```ts
// apps/playground/lib/transitionTypes.ts
export const transitionTypes = {
  toggleTab: 'toggle-tab',
  configPanel: 'config-panel',
} as const;

export type TransitionType = (typeof transitionTypes)[keyof typeof transitionTypes];
```

```ts
import { transitionTypes } from 'apps/playground/lib/transitionTypes';

startTransition(() => {
  addTransitionType(transitionTypes.toggleTab);
});
```

Why: consistent naming across modules, clearer intent in code, and safer uniqueness over time.