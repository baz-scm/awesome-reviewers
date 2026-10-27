---
title: Use named transition constants
description: 'When an identifier is shared across modules (e.g., transition/highlight
  “types”), avoid inline string literals. Instead:

  1) Define transition types as exported constants in a single shared module.'
repository: facebook/react#b9
label: Naming Conventions
language: TSX
comments_count: 2
repository_stars: 251891
---

When an identifier is shared across modules (e.g., transition/highlight “types”), avoid inline string literals. Instead:
1) Define transition types as exported constants in a single shared module.
2) Use clear, action-describing, uniquely scoped names (so future unrelated transitions don’t collide).

Example:

```ts
// apps/playground/lib/transitionTypes.ts
export const TRANSITION_TYPES = {
  TOGGLE_TAB: 'playground:toggle-tab',
  CONFIG_PANEL: 'playground:config-panel',
} as const;

export type TransitionType = (typeof TRANSITION_TYPES)[keyof typeof TRANSITION_TYPES];
```

Usage:

```ts
import { TRANSITION_TYPES } from 'apps/playground/lib/transitionTypes';

startTransition(() => {
  addTransitionType(TRANSITION_TYPES.TOGGLE_TAB);
});
```

This improves naming clarity, prevents mismatches between modules, and ensures identifiers remain unique over time.