---
title: Avoid effect escape hatches
description: When a UI selection/state is a deterministic consequence of current props/data
  (especially chained computations), don’t “fix it after paint” with `useEffect`.
  Doing so can show a stale frame, causing UI thrash.
repository: facebook/react#b7
label: React
language: JavaScript
comments_count: 5
repository_stars: 251888
---

When a UI selection/state is a deterministic consequence of current props/data (especially chained computations), don’t “fix it after paint” with `useEffect`. Doing so can show a stale frame, causing UI thrash.

Standards:
- If the next selection is derivable from current render inputs, compute/synchronize it during render (e.g., via a render-time update/previous-value pattern). Avoid `useEffect` as an escape hatch for consistency-critical UI.
- Don’t write to refs as a control-flow/state substitute during render. If you need to track previous props to decide an update, use state or a proper effect.
- Effects are fine for imperative work (scrolling/focusing) when the input is derived/external and you need an imperative API call. In that case, guard against “no selection” states and base the effect dependencies on the true derived values.

Example (bad: stale-frame selection):
```js
useEffect(() => {
  if (searchResults.length === 0) return;
  selectFiber(searchResults[0].id);
}, [searchResults]);
```

Example (good: keep selection consistent within the same render):
```js
const nextSelection = searchResults.length > 0 ? searchResults[0] : null;
if (nextSelection !== selectedFiber) {
  selectFiber(nextSelection?.id ?? null, nextSelection?.name ?? null);
}
```

If you’re tempted to use `useEffect` to “make two pieces of UI match,” first ask: “Can they be derived and synchronized during render so the first painted frame is already correct?”