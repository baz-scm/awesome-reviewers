---
title: Name Transition Types
description: When using identifier-like strings that must match across components
  (e.g., transition “type” names), avoid inline string literals. Define a semantically
  clear, unique constant set in a shared module and reuse it everywhere.
repository: facebook/react#b2
label: Naming Conventions
language: TSX
comments_count: 2
repository_stars: 251882
---

When using identifier-like strings that must match across components (e.g., transition “type” names), avoid inline string literals. Define a semantically clear, unique constant set in a shared module and reuse it everywhere.

Why:
- Improves naming clarity (the string communicates the action/purpose).
- Prevents drift across modules (single source of truth).
- Reduces future collisions (unique, domain-scoped identifiers).

How to apply:
1. Create a shared file that exports all allowed transition type names.
2. Use those exports instead of hardcoded strings in `addTransitionType(...)` calls.
3. Ensure each constant is uniquely scoped and action-oriented (e.g., includes the feature area and intent).

Example:
```ts
// apps/playground/lib/transitionTypes.ts
export const transitionTypes = {
  tabToggle: 'playground:tab-toggle',
  configPanel: 'playground:config-panel',
} as const;

export type TransitionType = (typeof transitionTypes)[keyof typeof transitionTypes];
```
```ts
import { transitionTypes } from 'apps/playground/lib/transitionTypes';

startTransition(() => {
  addTransitionType(transitionTypes.tabToggle);
});

startTransition(() => {
  addTransitionType(transitionTypes.configPanel);
});
```