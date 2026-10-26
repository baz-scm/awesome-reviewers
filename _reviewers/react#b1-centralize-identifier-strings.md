---
title: Centralize Identifier Strings
description: For any string identifier that is shared across modules (e.g., values
  passed to helpers like `addTransitionType`), avoid ad-hoc string literals. Instead,
  define a semantically meaningful, action-oriented constant in a shared module and
  reference that constant everywhere.
repository: facebook/react#b1
label: Naming Conventions
language: TSX
comments_count: 2
repository_stars: 251878
---

For any string identifier that is shared across modules (e.g., values passed to helpers like `addTransitionType`), avoid ad-hoc string literals. Instead, define a semantically meaningful, action-oriented constant in a shared module and reference that constant everywhere.

This improves naming consistency, prevents drift across components, and makes it easier to ensure future identifiers stay unique.

Example:

```ts
// apps/playground/lib/transitionTypes.ts
export const transitionTypes = {
  toggleTab: 'toggle-tab',
  configPanel: 'config-panel',
} as const;

export type TransitionType = (typeof transitionTypes)[keyof typeof transitionTypes];
```

```tsx
import { transitionTypes } from 'apps/playground/lib/transitionTypes';

startTransition(() => {
  addTransitionType(transitionTypes.toggleTab);
});
```