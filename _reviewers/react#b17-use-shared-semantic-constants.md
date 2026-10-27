---
title: Use shared semantic constants
description: When a string identifier is used across multiple components (e.g., transition/animation
  “type” values), don’t inline raw string literals at call sites. Define a single
  shared, exported constant with a semantic, action-describing name (and ensure it’s
  unique) in a common module, then import and reuse it everywhere.
repository: facebook/react#b17
label: Naming Conventions
language: TSX
comments_count: 2
repository_stars: 251891
---

When a string identifier is used across multiple components (e.g., transition/animation “type” values), don’t inline raw string literals at call sites. Define a single shared, exported constant with a semantic, action-describing name (and ensure it’s unique) in a common module, then import and reuse it everywhere.

Example:
```ts
// apps/playground/lib/transitionTypes.ts
export const TRANSITION_TYPES = {
  TOGGLE_TAB: 'toggle-tab',
  CONFIG_PANEL: 'config-panel',
} as const;
```
```ts
// TabbedWindow.tsx
import { TRANSITION_TYPES } from 'apps/playground/lib/transitionTypes';

startTransition(() => {
  addTransitionType(TRANSITION_TYPES.TOGGLE_TAB);
});
```
```ts
// ConfigEditor.tsx
import { TRANSITION_TYPES } from 'apps/playground/lib/transitionTypes';

startTransition(() => {
  addTransitionType(TRANSITION_TYPES.CONFIG_PANEL);
});
```

This improves naming clarity, prevents mismatched values across modules, and avoids future collisions with unrelated transition identifiers.