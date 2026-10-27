---
title: Semantic Constant Identifiers
description: 'When you use string identifiers that represent UI actions/behavior across
  multiple components, avoid inline string literals. Instead:

  1) Create exported constants in a shared module (e.g., `transitionTypes.ts`) so
  all usages stay consistent.'
repository: facebook/react#b16
label: Naming Conventions
language: TSX
comments_count: 2
repository_stars: 251891
---

When you use string identifiers that represent UI actions/behavior across multiple components, avoid inline string literals. Instead:
1) Create exported constants in a shared module (e.g., `transitionTypes.ts`) so all usages stay consistent.
2) Use semantic, action-descriptive names (the identifier should explain what it does).
3) Ensure identifiers are unique and future-safe (use a clear prefix/namespace).

Example:

```ts
// apps/playground/lib/transitionTypes.ts
export const transitionTypes = {
  toggleTab: 'tab/toggle',
  configPanel: 'config/panel',
} as const;

// TabbedWindow.tsx
addTransitionType(transitionTypes.toggleTab);

// ConfigEditor.tsx
addTransitionType(transitionTypes.configPanel);
```

This improves naming clarity (no opaque literals), consistency across modules (single source of truth), and prevents accidental collisions with new transitions later.