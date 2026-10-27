---
title: Use Shared Transition Constants
description: 'For any UI “type”/identifier that is referenced across components (e.g.,
  transition names passed as strings), avoid inline string literals. Instead:

  1) Define a single shared constants module (one source of truth).'
repository: facebook/react#b4
label: Naming Conventions
language: TSX
comments_count: 2
repository_stars: 251885
---

For any UI “type”/identifier that is referenced across components (e.g., transition names passed as strings), avoid inline string literals. Instead:
1) Define a single shared constants module (one source of truth).
2) Use semantically descriptive, action-oriented names (avoid overly generic labels).
3) Ensure values are unique/namespace-like to prevent collisions with future unrelated transitions.

Example:

```ts
// apps/playground/lib/transitionTypes.ts
export const transitionTypes = {
  TAB_TOGGLE: 'toggle-tab',
  CONFIG_PANEL_TOGGLE: 'toggle-config-panel',
} as const;
```

```tsx
import { transitionTypes } from 'apps/playground/lib/transitionTypes';

startTransition(() => {
  addTransitionType(transitionTypes.TAB_TOGGLE);
});
```

Apply this wherever the identifier must match across modules (rather than being purely local). This improves naming clarity, consistency, and prevents future identifier conflicts.