---
title: Sync derived UI in render
description: When some UI state is derived from other state/props (e.g., “selection
  depends on search results”), don’t use `useEffect` to patch it after paint. Instead,
  compute/derive it during render so the UI can’t briefly show stale intermediate
  state. Likewise, avoid mutating refs during render as a synchronization mechanism.
repository: facebook/react#b16
label: React
language: JavaScript
comments_count: 3
repository_stars: 251891
---

When some UI state is derived from other state/props (e.g., “selection depends on search results”), don’t use `useEffect` to patch it after paint. Instead, compute/derive it during render so the UI can’t briefly show stale intermediate state. Likewise, avoid mutating refs during render as a synchronization mechanism.

Use `useEffect` for imperative side-effects (scrolling, network/subscriptions), not for keeping derived selection/content in sync.

Example pattern (selection computed during render, not in an effect):

```js
function Component({searchText}) {
  const deferredText = useDeferredValue(searchText);
  const searchResults = useMemo(() => computeMatches(deferredText), [deferredText]);

  const [selectedIndex, setSelectedIndex] = useState(-1);
  const prevResultsRef = useRef(searchResults);

  // Render-time sync: keep selection consistent with results within the same render.
  if (prevResultsRef.current !== searchResults) {
    prevResultsRef.current = searchResults;
    setSelectedIndex(searchResults.length === 0 ? -1 : 0);
  }

  const selected = selectedIndex >= 0 ? searchResults[selectedIndex] : null;
  return <UI selected={selected} />;
}
```

If you must synchronize state, prefer render-time derivation/state updates guarded by previous-value checks, and keep imperative `useEffect` for non-UI-synchronization side-effects.