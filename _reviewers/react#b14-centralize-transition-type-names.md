---
title: Centralize transition type names
description: When an identifier (e.g., a transition “type”) is shared across multiple
  components/modules, avoid hard-coded string literals. Define it once as a centrally
  exported constant, and use a semantic, action-describing, uniquely namespaced name.
repository: facebook/react#b14
label: Naming Conventions
language: TSX
comments_count: 2
repository_stars: 251893
---

When an identifier (e.g., a transition “type”) is shared across multiple components/modules, avoid hard-coded string literals. Define it once as a centrally exported constant, and use a semantic, action-describing, uniquely namespaced name.

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
// TabbedWindow.tsx
import { transitionTypes } from 'apps/playground/lib/transitionTypes';

startTransition(() => {
  addTransitionType(transitionTypes.toggleTab);
});

// ConfigEditor.tsx
import { transitionTypes } from 'apps/playground/lib/transitionTypes';

startTransition(() => {
  addTransitionType(transitionTypes.configPanel);
});
```

This ensures consistent naming across usages and reduces the risk of collisions as new transitions are added.