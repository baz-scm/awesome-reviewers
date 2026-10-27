---
title: Derive state during render
description: Prefer computing derived values directly in the render function over
  synchronizing them with `useEffect`. Effects run after the browser paints, so using
  them to adjust state based on a prop/data change causes a visible flash of stale
  UI before the correction lands (UI thrashing). If you need to "reset" or recompute
  state when an input changes, do it during...
repository: facebook/react#b18
label: React
language: JavaScript
comments_count: 7
repository_stars: 251889
---

Prefer computing derived values directly in the render function over synchronizing them with `useEffect`. Effects run after the browser paints, so using them to adjust state based on a prop/data change causes a visible flash of stale UI before the correction lands (UI thrashing). If you need to "reset" or recompute state when an input changes, do it during render using the previous-value comparison pattern with `useState` (not `useRef`, since writing to a ref during render is unsafe):

```js
const [prevCommitData, setPrevCommitData] = useState(commitData);
if (prevCommitData !== commitData) {
  setPrevCommitData(commitData);
  selectCommitIndex(commitData.length > 0 ? 0 : null);
}
```
This is not a "cascading update" problem because state updates during render are applied immediately, before paint, unlike updates scheduled from effects.

When the derived computation is expensive (e.g. searching/filtering a large tree), keep any controlled input updates synchronous so typing stays responsive, and derive the expensive result from a deferred value so it runs at transition priority without blocking the input:

```js
const setSearchText = useCallback((text) => {
  setSearchTextState(text); // synchronous, keeps input responsive
}, []);

const deferredSearchText = useDeferredValue(searchText);
const searchResults = useMemo(
  () => findMatches(deferredSearchText), // runs at transition priority
  [deferredSearchText],
);
```
Consider surfacing a pending indicator (`searchText !== deferredSearchText`) so users know a result is still catching up.

Finally, minimize the number of effects and their dependencies. If an effect only needs to read the latest value of some state without re-subscribing when that state changes (e.g. a keydown listener that checks `isProfiling`), extract that logic into `useEffectEvent` instead of adding it as a dependency — this avoids tearing down and recreating subscriptions on every unrelated state change.

Before reaching for `useEffect`, check whether the logic can be expressed as a computation during render, an event handler, or a transition — effects should be reserved for truly synchronizing with external systems.