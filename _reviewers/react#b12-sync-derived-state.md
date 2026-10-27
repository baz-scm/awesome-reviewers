---
title: Sync Derived State
description: When UI correctness depends on derived values, update it in the same
  render instead of patching it in `useEffect` after the browser has already painted.
repository: facebook/react#b12
label: React
language: JavaScript
comments_count: 5
repository_stars: 251896
---

When UI correctness depends on derived values, update it in the same render instead of patching it in `useEffect` after the browser has already painted.

**Rules**
- Avoid “escape-hatch” `useEffect` chains to keep two pieces of state in sync (e.g., selection should always match search results). If there’s a moment where the UI can show stale/incorrect selection for one frame, move the computation/update into render (accepting a possible cascading re-render).
- Use the intended async/Suspense primitives rather than deprecated hacks.
  - Prefer `React.use(promise)` over throwing Promises (including in tests).
- Ensure server-only APIs fail fast when accidentally imported/used in client contexts; don’t rely on silent no-ops.

**Example (selection/search sync)**
```js
function ProfileSearch({searchText}) {
  const deferred = useDeferredValue(searchText);
  const results = useMemo(() => computeMatches(deferred), [deferred]);

  // Keep selection consistent with results *during render*, not after paint.
  const [selectedIndex, setSelectedIndex] = useState(-1);
  const safeIndex = results.length === 0 ? -1 :
    (selectedIndex < 0 || selectedIndex >= results.length ? 0 : selectedIndex);

  const selected = safeIndex === -1 ? null : results[safeIndex];

  // No useEffect needed just to “catch up” selection.
  return <UI selected={selected} />;
}
```

**Why**: render-time consistency prevents one-frame UI thrash and avoids subtle timing bugs in keyboard/mouse navigation and profiler-style controlled state.