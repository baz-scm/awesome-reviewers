---
title: Consistent Semantic Identifiers
description: 'Use semantic, globally consistent names for shared identifiers—especially
  string “type” values used across components.


  - Prefer constants over inline string literals for shared types (e.g., transition
  types). Centralize them in a shared module (example below).'
repository: facebook/react#b5
label: Naming Conventions
language: TSX
comments_count: 3
repository_stars: 251886
---

Use semantic, globally consistent names for shared identifiers—especially string “type” values used across components.

- Prefer constants over inline string literals for shared types (e.g., transition types). Centralize them in a shared module (example below).
- Choose names that describe the action/state (e.g., prefer `toggleTab` over a generic or ambiguous label) and ensure they’re unique to avoid collisions with future unrelated transitions.
- Keep import/identifier style consistent across files within the workspace (don’t mix differing import path conventions until an aliasing strategy is agreed).

Example (centralized transition types):

```ts
// apps/playground/lib/transitionTypes.ts
export const transitionTypes = {
  tabToggle: 'toggle-tab',
  configPanel: 'config-panel',
} as const;

export type TransitionType = (typeof transitionTypes)[keyof typeof transitionTypes];
```

```tsx
import {transitionTypes} from 'apps/playground/lib/transitionTypes';

startTransition(() => {
  addTransitionType(transitionTypes.tabToggle);
});
```
