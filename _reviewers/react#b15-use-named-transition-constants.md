---
title: Use named transition constants
description: When a string identifier is reused across multiple modules (e.g., transition
  types), define it once as a shared constant and reference the constant everywhere.
  Choose an intent-based, semantically clear name and ensure it’s unique (e.g., feature-
  or action-prefixed) to avoid future collisions.
repository: facebook/react#b15
label: Naming Conventions
language: TSX
comments_count: 2
repository_stars: 251891
---

When a string identifier is reused across multiple modules (e.g., transition types), define it once as a shared constant and reference the constant everywhere. Choose an intent-based, semantically clear name and ensure it’s unique (e.g., feature- or action-prefixed) to avoid future collisions.

Example:
```ts
// apps/playground/lib/transitionTypes.ts
export const transitionTypes = {
  tab: 'toggle-tab',
  configPanel: 'config-panel',
} as const;

// TabbedWindow.tsx
import { transitionTypes } from 'apps/playground/lib/transitionTypes';

startTransition(() => {
  addTransitionType(transitionTypes.tab);
});

// ConfigEditor.tsx
import { transitionTypes } from 'apps/playground/lib/transitionTypes';

startTransition(() => {
  addTransitionType(transitionTypes.configPanel);
});
```