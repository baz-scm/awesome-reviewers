---
title: Prefer Render Sync
description: When you need to keep UI state consistent with other state/props (derived
  data), perform the synchronization during render (or via derived values like `useMemo`),
  not in `useEffect`. Reserve `useEffect` for true side effects—especially when you
  must call an imperative external API that can’t be represented as pure render output.
  This avoids “one frame...
repository: facebook/react#b15
label: React
language: JavaScript
comments_count: 5
repository_stars: 251891
---

When you need to keep UI state consistent with other state/props (derived data), perform the synchronization during render (or via derived values like `useMemo`), not in `useEffect`. Reserve `useEffect` for true side effects—especially when you must call an imperative external API that can’t be represented as pure render output. This avoids “one frame behind” UI thrash where the browser paints a stale state.

Decision checklist:
- If the goal is “make derived UI selection match derived results” → compute/choose the correct state in render.
- If the goal is “call an imperative API” (scroll, focus, subscriptions, DOM measurement that isn’t pure output) → use `useEffect` and synchronize with derived inputs.
- Keep effect dependencies minimal; avoid repeatedly tearing down/recreating listeners when possible.

Example (render-time sync):
```js
function ProfilerSearchSync({searchResults, searchIndex, selectFiber}) {
  // Derived selection must not lag behind what’s rendered.
  // Do the selection logic during render so there’s no post-paint frame mismatch.
  if (searchResults.length === 0) {
    if (/* deferredSearchText !== '' */) selectFiber(null, null);
  } else {
    const index = searchIndex < 0 || searchIndex >= searchResults.length ? 0 : searchIndex;
    const match = searchResults[index];
    selectFiber(match.id, match.name);
  }
  return null; // selection happens via the sync path
}
```

Example (effect-time imperative sync):
```js
function ScrollToSelected({selectedFiberID, selectedChartNodeIndex}) {
  const listRef = React.useRef(null);

  React.useEffect(() => {
    // Run the imperative side effect only when inputs are ready.
    if (selectedFiberID !== null && listRef.current !== null) {
      listRef.current.scrollToItem(selectedChartNodeIndex, 'smart');
    }
  }, [selectedFiberID, selectedChartNodeIndex]);

  return <div ref={listRef} />;
}
```