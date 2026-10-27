---
title: Render-atomic React State
description: When UI correctness depends on derived state being consistent for the
  current paint, don’t “sync” it with a `useEffect` escape hatch. Instead, compute
  and apply the derived selection/state during render (or restructure so the invariant
  holds), and always follow React’s contracts for hooks and async.
repository: facebook/react#b13
label: React
language: JavaScript
comments_count: 5
repository_stars: 251893
---

When UI correctness depends on derived state being consistent for the current paint, don’t “sync” it with a `useEffect` escape hatch. Instead, compute and apply the derived selection/state during render (or restructure so the invariant holds), and always follow React’s contracts for hooks and async.

**Standards**
1. **Frame-atomic derived state**: If a change to inputs (search text/results, selection) must not show stale UI for a frame, avoid `useEffect` to update the “selected” state after paint. Prefer updating selection during render (using the existing state/prev-value pattern) so the UI and derived state are consistent in the same render.
2. **No hooks after early returns**: Ensure all hooks are called unconditionally and in the same order on every render. If there’s an early return, move hooks above it.
3. **Use supported async patterns**: Prefer `use(promise)` over directly throwing Promises in tests/usage paths that will be deprecated.
4. **Don’t mutate refs to emulate state updates in render**: Writing to refs during render to drive behavior is unsafe; use state updates (or effects) with correct scoping.

**Example (render-time selection instead of useEffect)**
```js
function ProfileSearchController({searchText, searchResults, searchIndex, selectFiber}) {
  // Avoid: useEffect(() => selectFiber(...), [searchResults, searchIndex])

  const resolvedIndex =
    searchIndex < 0 || searchIndex >= searchResults.length ? 0 : searchIndex;
  const match = searchResults.length > 0 ? searchResults[resolvedIndex] : null;

  // Update selection during render so it’s consistent with what the user sees.
  // (Implementation detail: use prev-value pattern / existing state sync in the file.)
  if (match) {
    selectFiber(match.id, match.name);
  } else {
    selectFiber(null, null);
  }

  return null;
}
```

Apply this mindset whenever you see a `useEffect` used to “keep selection/results in sync” or to prevent one-frame UI thrash—restructure so the invariant is maintained during render, and keep hooks/async usage compliant.