---
title: Centralize Transition Type Names
description: Use shared, descriptively named constants (from a single module) instead
  of inline string literals for transition “type” identifiers. Names should be action/context-oriented
  and globally unique to prevent collisions as the codebase grows.
repository: facebook/react#b8
label: Naming Conventions
language: TSX
comments_count: 2
repository_stars: 251889
---

Use shared, descriptively named constants (from a single module) instead of inline string literals for transition “type” identifiers. Names should be action/context-oriented and globally unique to prevent collisions as the codebase grows.

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
  addTransitionType(transitionTypes.configPanel);
});
```

Apply this whenever a transition type is referenced in multiple components/modules or when the string would be easy to mistype or collide with future transitions.