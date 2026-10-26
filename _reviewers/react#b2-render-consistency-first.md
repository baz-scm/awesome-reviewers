---
title: Render Consistency First
description: When state must stay logically consistent (e.g., search results + selected
  item, derived indices + imperative UI like scrolling), compute it so the UI is correct
  on the very first painted frame.
repository: facebook/react#b2
label: React
language: JavaScript
comments_count: 6
repository_stars: 251882
---

When state must stay logically consistent (e.g., search results + selected item, derived indices + imperative UI like scrolling), compute it so the UI is correct on the very first painted frame.

**Guideline**
- Prefer deriving related UI state *during render* (or via memoized/derived values) so selection/UI never lags behind computations.
- Use `useEffect` only to synchronize with **external systems** (DOM imperative APIs, subscriptions, timers) where “after paint” is acceptable/necessary.
- If you must imperatively update (e.g., `scrollToItem`), keep it tightly scoped to the derived values it depends on.
- Never violate the Rules of Hooks: don’t conditionally return before all hooks are called.

**Anti-pattern (causes stale frame / thrash)**
```js
useEffect(() => {
  // selection updates after paint, UI may show stale selection for a frame
  selectFiber(match.id);
}, [searchResults, searchIndex]);
```

**Preferred pattern (keep selection + results in lockstep)**
```js
const deferredText = useDeferredValue(searchText);
const results = useMemo(() => computeMatches(deferredText), [deferredText]);
const safeIndex = results.length === 0 ? -1 : clamp(searchIndex, 0, results.length - 1);
const selectedId = safeIndex >= 0 ? results[safeIndex].id : null;
// derive/commit selection synchronously as part of render logic
```

**Rules of Hooks reminder**
```js
function Component({flag}) {
  const [x] = useState(0);
  useEffect(() => {}, []);
  if (!flag) return <div />; // return only after hooks
  return <div>{x}</div>;
}
```

**Effect/Subscription hygiene**
- Avoid resubscribing listeners on every render via large dependency sets; keep dependencies minimal or use an event-stable pattern (e.g., `useEffectEvent`).