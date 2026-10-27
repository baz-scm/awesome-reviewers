---
title: Correct React Semantics
description: When writing React code, align with React’s execution model so that (a)
  misuse fails early, (b) derived state and UI stay in sync in the same render, and
  (c) hook/promise semantics follow supported rules.
repository: facebook/react#b14
label: React
language: JavaScript
comments_count: 7
repository_stars: 251893
---

When writing React code, align with React’s execution model so that (a) misuse fails early, (b) derived state and UI stay in sync in the same render, and (c) hook/promise semantics follow supported rules.

### Apply this standard
1) **Enforce server/client boundaries (early failure)**
- Don’t expose server-only helpers/APIs to client builds. Prefer making client imports error (instead of silent no-ops) so incorrect usage is caught immediately.

2) **Use supported promise patterns**
- Prefer `React.use(promise)` over “throwing promises” in component code.
- Keep `use()` call diagnostics distinct (uncached-promise vs async-component) by ensuring the callsite matches the intended scenario.

3) **Keep render-critical coordination out of `useEffect`**
- If updates are a chain where the next UI must match the same derived data, don’t use `useEffect` just to “sync after paint” (it can cause a 1-frame stale UI).
- Derive the needed values and perform the selection/state transitions during render using existing previous-value patterns (if the codebase already uses them).

4) **Respect Rules of Hooks & dependency correctness**
- Never early-return before all hooks for that component path.
- Ensure dependency arrays include values that can change (e.g., refs).

5) **Avoid unsafe render-time mutations**
- Don’t update refs/state in render as a substitute for an effect; if you need to respond to prop changes, use a safe state-driven approach.

### Example: prefer same-render coordination over “after paint” effects
```js
function ProfilerSearchSync({searchText, searchResults, searchIndex, selectFiber}) {
  // BAD: would run after paint and can briefly show stale selection
  // useEffect(() => { ...selectFiber(...) }, [searchResults, searchIndex]);

  // GOOD: keep selection consistent with derived inputs in the same render
  const effectiveIndex =
    searchIndex < 0 || searchIndex >= searchResults.length ? 0 : searchIndex;
  const match = searchResults.length === 0 ? null : searchResults[effectiveIndex];

  // Use the component’s established “previous value” pattern if needed.
  if (match == null) {
    // selectFiber(null, null)
  } else {
    // selectFiber(match.id, match.name)
  }

  return null;
}
```

This standard reduces hydration/UI desync bugs, prevents noisy or confusing runtime warnings, and keeps behavior predictable across renderers and environments.