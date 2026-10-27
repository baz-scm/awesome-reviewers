---
title: Derived State in Render
description: 'Prefer rendering-time derivation over effect-based synchronization.


  **Do**

  - Keep *logically coupled* state (e.g., “search results” and “selected index/fiber”)
  consistent during the same render. Derive results with `useMemo` and reconcile selection
  in render so the first paint can’t be stale.'
repository: facebook/react#b9
label: React
language: JavaScript
comments_count: 5
repository_stars: 251891
---

Prefer rendering-time derivation over effect-based synchronization.

**Do**
- Keep *logically coupled* state (e.g., “search results” and “selected index/fiber”) consistent during the same render. Derive results with `useMemo` and reconcile selection in render so the first paint can’t be stale.
- Use `useEffect` for **imperative side effects** that can’t happen during render (e.g., `scrollToItem`).
- Avoid updating refs/state during render (e.g., writing to a `useRef` to “track previous props”); use state/effects instead.
- Follow the Rules of Hooks: never introduce conditional hook execution via early returns.

**Don’t**
- Use `useEffect` as an “escape hatch” to fix mismatches after paint (it can cause a visible one-frame thrash).

**Example (render-time sync + effect for imperative scroll)**
```js
function Example({searchText}) {
  const deferred = useDeferredValue(searchText);
  const results = useMemo(() => computeMatches(deferred), [deferred]);

  // Keep selection consistent with results in the same render.
  const [selectedIndex, setSelectedIndex] = useState(-1);
  const safeIndex = results.length === 0 ? -1 :
    selectedIndex < 0 || selectedIndex >= results.length ? 0 : selectedIndex;

  // Imperative sync belongs in an effect.
  useEffect(() => {
    if (safeIndex >= 0) {
      listRef.current?.scrollToItem(safeIndex, 'smart');
    }
  }, [safeIndex]);

  return null;
}
```