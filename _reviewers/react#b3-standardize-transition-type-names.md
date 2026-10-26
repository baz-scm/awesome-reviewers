---
title: Standardize Transition Type Names
description: 'For any cross-module UI “type” identifiers (e.g., transition/highlight
  names), do not use ad-hoc string literals in components. Instead:


  1) Centralize them in a shared module (e.g., `apps/playground/lib/transitionTypes.ts`).'
repository: facebook/react#b3
label: Naming Conventions
language: TSX
comments_count: 2
repository_stars: 251883
---

For any cross-module UI “type” identifiers (e.g., transition/highlight names), do not use ad-hoc string literals in components. Instead:

1) Centralize them in a shared module (e.g., `apps/playground/lib/transitionTypes.ts`).
2) Use descriptive, action-based names (e.g., `toggle-tab` instead of vague labels).
3) Ensure uniqueness with a consistent prefix/namespace so unrelated transitions can’t collide.

Example:

```ts
// apps/playground/lib/transitionTypes.ts
export const transitionTypes = {
  tab: 'toggle-tab',
  configPanel: 'config-panel',
} as const;
```

```tsx
import {transitionTypes} from 'apps/playground/lib/transitionTypes';

startTransition(() => {
  addTransitionType(transitionTypes.tab);
});
```

This keeps naming consistent across usages, improves identifier clarity, and prevents future collisions when adding new transitions.