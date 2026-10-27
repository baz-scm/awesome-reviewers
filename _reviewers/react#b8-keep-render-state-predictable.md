---
title: Keep render-state predictable
description: 'Ensure React components remain predictable by keeping render logic pure
  and by making state transitions (especially resets) fully intentional.


  **Rules**'
repository: facebook/react#b8
label: React
language: TSX
comments_count: 2
repository_stars: 251889
---

Ensure React components remain predictable by keeping render logic pure and by making state transitions (especially resets) fully intentional.

**Rules**
1. **Don’t read refs during render.** If you need “last valid” data, compute it in a safer place (event handler, reducer/store update, or effect) and store the result in state that the render can read.
2. **Gate updates outside render.** Perform validation/compilation in the store/update path, and only commit the property when the input is valid.
3. **Force resets must clear client state.** When “reset playground” is triggered, reset the entire relevant client state slice; only preserve fields if that preservation is explicitly required.

**Example pattern (gate updates outside render)**
```ts
// pseudo-store reducer/update
function updateAppliedOptions(state, action) {
  const next = action.payload;
  const formatted = tryFormat(next); // validate/compute here
  if (!formatted) return state; // keep previous valid state
  return { ...state, formattedAppliedOptions: formatted };
}
```
Then the component render simply reads `state.formattedAppliedOptions`—no ref reads and no render-time validation/compilation.

This prevents React purity violations and ensures reset behavior matches user expectations (a true wipe, not a partial state carryover).