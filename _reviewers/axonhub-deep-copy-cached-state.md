---
title: Deep-copy cached state
description: When cached data (e.g., `row.settings`) is used to initialize mutable
  UI state (forms, editors, draft objects), do not pass cached object references directly.
  Always deep-clone cached objects on entry to editable state to prevent unintended
  cache mutations and ensure copied/duplicated initialization is isolated.
repository: looplj/axonhub
label: Caching
language: TSX
comments_count: 2
repository_stars: 4808
---

When cached data (e.g., `row.settings`) is used to initialize mutable UI state (forms, editors, draft objects), do not pass cached object references directly. Always deep-clone cached objects on entry to editable state to prevent unintended cache mutations and ensure copied/duplicated initialization is isolated.

Example pattern:
```ts
const settings = currentRow.settings
  ? structuredClone(currentRow.settings)
  : undefined;

// use `settings` as initial/editable state
const initialValues = {
  ...,
  settings,
};
```
If `settings` is nested, prefer `structuredClone` (or an equivalent deep-clone) over shallow spreads to guarantee full isolation.