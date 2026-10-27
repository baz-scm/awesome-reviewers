---
title: Synchronous Hooks And Suspense
description: 'Adopt a “correct semantics first, paint-consistent next” standard:


  1) Use the right Suspense primitive

  - When working with promises in React components/tests, prefer `use(promise)` over
  throwing promises (where applicable).'
repository: facebook/react#b4
label: React
language: JavaScript
comments_count: 6
repository_stars: 251885
---

Adopt a “correct semantics first, paint-consistent next” standard:

1) Use the right Suspense primitive
- When working with promises in React components/tests, prefer `use(promise)` over throwing promises (where applicable).

2) Don’t create new promises inside render-time memo/initialization
- Avoid creating new Promises inside state initializer functions or `useMemo` (hoist creation outside the component / into an initializer that doesn’t create fresh promises per render in unsupported ways).

3) Never return early before Hooks
- Ensure all Hooks are called unconditionally on every render (no early returns before `useState`/`useEffect`/etc.).

4) Avoid `useEffect` as an escape hatch for UI correctness
- If a state/selection update must be reflected without an extra “stale frame”, derive and update it synchronously during render rather than in `useEffect` (prevents UI thrashing).

Example pattern (derive synchronously, keep Hooks unconditional):
```js
function Component({query}) {
  // Hooks always at top
  const [searchText, setSearchText] = useState(query);
  const deferredQuery = useDeferredValue(searchText);

  const results = useMemo(() => findMatches(deferredQuery), [deferredQuery]);
  const selectedIndex = results.length === 0 ? -1 : 0;

  // Update selection synchronously (no effect needed for correctness)
  // ...render UI based on results/selectedIndex...

  return <div>{results.length ? results[selectedIndex].name : 'No results'}</div>;
}
```

If an update cannot be expressed as a pure derivation and truly needs an after-paint imperative sync (e.g., scrolling), isolate it in `useEffect`, but don’t use `useEffect` to “fix” what users should already see in the current render.