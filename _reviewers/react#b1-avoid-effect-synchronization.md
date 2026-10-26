---
title: Avoid Effect Synchronization
description: When a piece of UI state is purely derived from other state/props, update
  it synchronously during render (or during the same commit) instead of using `useEffect`
  to “chase” derived values. Using `useEffect` as a synchronization mechanism can
  produce a brief stale frame (UI thrash). Effects are appropriate when you must synchronize
  with an imperative API...
repository: facebook/react#b1
label: React
language: JavaScript
comments_count: 4
repository_stars: 251878
---

When a piece of UI state is purely derived from other state/props, update it synchronously during render (or during the same commit) instead of using `useEffect` to “chase” derived values. Using `useEffect` as a synchronization mechanism can produce a brief stale frame (UI thrash). Effects are appropriate when you must synchronize with an imperative API (e.g., scrolling), and those effects should be driven by derived values with correct guards.

Do:
- Derive selection/display state from inputs in render.
- If you need to bridge to an imperative API, call it in an effect with clear dependencies.
- Avoid mutating refs during render as a way to trigger synchronization; prefer React state updates or safe derived patterns.

Example (avoid `useEffect` for derived selection):
```js
function Controller({searchText}) {
  const deferredText = useDeferredValue(searchText);
  const results = useMemo(() => computeResults(deferredText), [deferredText]);

  // Synchronous in render to keep selection and results consistent.
  const nextSelected = results.length === 0 ? null : results[Math.min(prevIndex, results.length - 1)];

  // Use a render-safe previous-value pattern for index/selection if needed.
  // (The key point: don’t wait for an effect to update selection after paint.)

  return <View selected={nextSelected} />;
}
```

Example (allowed imperative sync):
```js
useEffect(() => {
  if (selectedIndex == null) return;
  listRef.current?.scrollToItem(selectedIndex, 'smart');
}, [selectedIndex]);
```