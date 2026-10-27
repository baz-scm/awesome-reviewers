---
title: Shared Transition Type Names
description: For any cross-component “type” string (e.g., values passed to `addTransitionType`),
  avoid ad-hoc string literals. Create named exports in a shared module, use action-descriptive
  names, and ensure the identifiers are unique across features.
repository: facebook/react#b6
label: Naming Conventions
language: TSX
comments_count: 2
repository_stars: 251888
---

For any cross-component “type” string (e.g., values passed to `addTransitionType`), avoid ad-hoc string literals. Create named exports in a shared module, use action-descriptive names, and ensure the identifiers are unique across features.

Example:

```ts
// apps/playground/lib/transitionTypes.ts
export const TransitionTypes = {
  toggleTab: 'toggle-tab',
  configPanel: 'config-panel',
  // keep adding globally-unique, semantically descriptive names
} as const;
```

```ts
import {TransitionTypes} from 'apps/playground/lib/transitionTypes';

startTransition(() => {
  addTransitionType(TransitionTypes.toggleTab);
});
```

Benefits: consistent naming across modules, easier refactors, and prevention of collisions with future transition types.