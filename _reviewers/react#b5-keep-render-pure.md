---
title: Keep Render Pure
description: In React, treat render as a pure function of props/state. Don’t derive
  UI output from mutable ref history during render; instead, push validation and state-transition
  policy into your state layer (store/actions), including “force reset” semantics.
repository: facebook/react#b5
label: React
language: TSX
comments_count: 2
repository_stars: 251886
---

In React, treat render as a pure function of props/state. Don’t derive UI output from mutable ref history during render; instead, push validation and state-transition policy into your state layer (store/actions), including “force reset” semantics.

How to apply:
- Avoid using refs to supply fallback values inside the render path. If you need “last valid options,” store that value in state (or update the store only when the new value is valid).
- When resetting, decide reset semantics in the action: a true “force reset” should clear client/UI state rather than preserving flags.

Example pattern (validation in store, not in render):
```ts
// In your store/action layer
function setAppliedOptions(appliedOptions: unknown) {
  if (!appliedOptions) return; // or dispatch to clear explicitly
  const formatted = prettyFormat(appliedOptions, {
    printFunctionName: false,
    printBasicPrototype: false,
  });

  // Commit only when valid
  dispatchStore({
    type: 'setStore',
    payload: { store: { ...getStore(), formattedAppliedOptions: formatted } },
  });
}

// In the component render: just read derived state
// const formattedAppliedOptions = store.formattedAppliedOptions;
```

For reset:
```ts
// Force reset clears all client state (including toggles)
dispatchStore({
  type: 'resetStore',
  payload: { store: defaultStore } // do not preserve showInternals
});
```