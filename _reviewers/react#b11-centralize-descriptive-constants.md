---
title: Centralize descriptive constants
description: When a string literal (or similar identifier) is used as a semantic “type”
  across multiple modules—especially for UI/transition behavior—define it once as
  a shared constant and reuse it everywhere.
repository: facebook/react#b11
label: Naming Conventions
language: TSX
comments_count: 2
repository_stars: 251894
---

When a string literal (or similar identifier) is used as a semantic “type” across multiple modules—especially for UI/transition behavior—define it once as a shared constant and reuse it everywhere.

Guidelines:
- Prefer intent-descriptive names (e.g., include the action, not just the UI element).
- Centralize the definitions in a shared module so all callers use the same spelling.
- Choose values/names that are unique enough to avoid collisions with future unrelated transitions.

Example:
```ts
// apps/playground/lib/transitionTypes.ts
export const transitionTypes = {
  tab: 'toggle-tab',
  configPanel: 'config-panel',
} as const;

export type TransitionType = (typeof transitionTypes)[keyof typeof transitionTypes];
```
```ts
// TabbedWindow.tsx (usage)
import { transitionTypes } from 'apps/playground/lib/transitionTypes';

startTransition(() => {
  addTransitionType(transitionTypes.tab);
});

// ConfigEditor.tsx (usage)
import { transitionTypes } from 'apps/playground/lib/transitionTypes';

startTransition(() => {
  addTransitionType(transitionTypes.configPanel);
});
```
This improves naming consistency, makes identifiers easier to search, and prevents subtle mismatches caused by duplicated string literals.