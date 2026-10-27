---
title: Avoid Effect Sync Thrash
description: When keeping UI in sync with derived data (e.g., selection that depends
  on computed results), don’t use `useEffect` as a synchronization bridge—effects
  run after paint and can produce a brief stale frame (UI thrashing). Instead, compute
  the derived inputs during render and update any dependent selection/state in a render-safe
  way.
repository: facebook/react#b5
label: React
language: JavaScript
comments_count: 5
repository_stars: 251886
---

When keeping UI in sync with derived data (e.g., selection that depends on computed results), don’t use `useEffect` as a synchronization bridge—effects run after paint and can produce a brief stale frame (UI thrashing). Instead, compute the derived inputs during render and update any dependent selection/state in a render-safe way.

Use `useEffect` only for true side effects (timers, event subscriptions, IO) or to call imperative APIs where a one-frame delay is acceptable and the effect is narrowly scoped.

Example pattern (selection derived from search results):
```js
// Bad: effect runs after paint -> can briefly show stale selection
useEffect(() => {
  if (results.length === 0) setSelected(null);
  else setSelected(results[clampedIndex]);
}, [results, index]);

// Good: derive and synchronize during render
const derivedSelected = results.length === 0 ? null : results[clampedIndex];
// then update selection via render-time/state sync strategy used in this component
// (e.g., a render-driven “previous value” pattern already present in the file)
```

Also:
- Keep effect logic minimal: for event listeners/keyboard shortcuts, avoid re-subscribing on every state change; prefer stable callbacks (e.g. `useEffectEvent`) and tighter dependencies.
- Don’t write to refs during render to mimic prop-driven synchronization when it can lead to unsafe behavior; prefer state derived via render.
