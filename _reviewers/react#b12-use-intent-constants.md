---
title: Use Intent Constants
description: For cross-module semantic identifiers (e.g., transition “types”), avoid
  inline magic strings. Define them as centrally exported constants/enums with intent-revealing
  names, and ensure the names are unique for the action they represent.
repository: facebook/react#b12
label: Naming Conventions
language: TSX
comments_count: 2
repository_stars: 251896
---

For cross-module semantic identifiers (e.g., transition “types”), avoid inline magic strings. Define them as centrally exported constants/enums with intent-revealing names, and ensure the names are unique for the action they represent.

Example:
```ts
// apps/playground/lib/transitionTypes.ts
export const transitionTypes = {
  tab: 'toggle-tab',        // intent-revealing
  configPanel: 'config-panel',
} as const;

export type TransitionType = (typeof transitionTypes)[keyof typeof transitionTypes];
```

Usage:
```ts
import { transitionTypes } from 'apps/playground/lib/transitionTypes';

startTransition(() => {
  addTransitionType(transitionTypes.tab);
});
```

Apply this whenever the value is referenced from multiple components/modules or when the string name is part of a shared convention; centralizing the definitions keeps naming consistent and prevents future collisions.