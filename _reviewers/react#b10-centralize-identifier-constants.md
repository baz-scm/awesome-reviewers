---
title: Centralize Identifier Constants
description: When an identifier is used across multiple components/modules (especially
  string-based labels), define it once as a shared, exported constant—using a clear,
  action-descriptive name—and reuse it everywhere. This prevents drift, improves naming
  clarity, and avoids collisions with future unrelated identifiers.
repository: facebook/react#b10
label: Naming Conventions
language: TSX
comments_count: 2
repository_stars: 251894
---

When an identifier is used across multiple components/modules (especially string-based labels), define it once as a shared, exported constant—using a clear, action-descriptive name—and reuse it everywhere. This prevents drift, improves naming clarity, and avoids collisions with future unrelated identifiers.

Example:
```ts
// apps/playground/lib/transitionTypes.ts
export const transitionTypes = {
  tab: 'tab',
  'config-panel': 'config-panel',
} as const;

export type TransitionType = (typeof transitionTypes)[keyof typeof transitionTypes];

// usage
import { transitionTypes } from 'apps/playground/lib/transitionTypes';

startTransition(() => {
  addTransitionType(transitionTypes['config-panel']);
});
```

If a current string literal feels ambiguous (e.g., it doesn’t describe the action), rename the constant to something more specific (e.g., `'toggle-tab'`-style) before centralizing it.