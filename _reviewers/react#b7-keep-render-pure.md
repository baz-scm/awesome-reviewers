---
title: Keep Render Pure
description: 'Treat React render as a pure function of props/state.


  - Don’t use refs as render-time fallbacks for validation/compilation results. Instead,
  validate/compute the derived value before updating state (e.g., in the store/action
  that receives the update) and only commit valid results.'
repository: facebook/react#b7
label: React
language: TSX
comments_count: 2
repository_stars: 251888
---

Treat React render as a pure function of props/state.

- Don’t use refs as render-time fallbacks for validation/compilation results. Instead, validate/compute the derived value before updating state (e.g., in the store/action that receives the update) and only commit valid results.
- For “force reset” UX, reset actions should fully clear client state (including optional UI flags) unless the product explicitly requires preservation.

Example pattern (compute/validate before committing):
```ts
// inside an action/reducer/thunk, not inside a component render
function setAppliedOptions(nextOptions) {
  const formatted = prettyFormat(nextOptions, {
    printFunctionName: false,
    printBasicPrototype: false,
  });

  // if invalid, skip updating the store value
  if (!formatted) return;

  dispatch({ type: 'setStore', payload: { appliedOptions: nextOptions, formattedAppliedOptions: formatted } });
}

// force reset: clear everything
function forceReset() {
  dispatch({ type: 'setStore', payload: { store: defaultStore /* no state preservation */ } });
}
```