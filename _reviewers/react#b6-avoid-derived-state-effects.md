---
title: Avoid Derived State Effects
description: 'Keep render output and derived state synchronized without relying on
  `useEffect` “escape hatches” that can leave a stale frame visible.


  **Rules**

  1. **If the problem is render correctness** (e.g., selection must always match the
  current derived results), prefer deriving during render or synchronizing within
  the same render cycle, rather than updating...'
repository: facebook/react#b6
label: React
language: JavaScript
comments_count: 4
repository_stars: 251888
---

Keep render output and derived state synchronized without relying on `useEffect` “escape hatches” that can leave a stale frame visible.

**Rules**
1. **If the problem is render correctness** (e.g., selection must always match the current derived results), prefer deriving during render or synchronizing within the same render cycle, rather than updating selection in a passive effect that runs after paint.
2. **Use `useEffect` for imperative side effects**, not for driving primary UI consistency (e.g., scroll a list when selection changes).
3. **Never return before all hooks run**—call hooks unconditionally at the top of the component.

**Example (avoid a stale post-paint selection frame)**
```jsx
function ProfilerSearch({searchText, commitData}) {
  const deferredText = React.useDeferredValue(searchText);

  const searchResults = React.useMemo(() => {
    // derive results from deferredText + commitData
    return computeMatches(deferredText, commitData);
  }, [deferredText, commitData]);

  // Keep selected index/name consistent with derived results *during render*.
  // (Instead of updating selection in a useEffect that runs after paint.)
  const [selected, setSelected] = React.useState(null);
  if (searchResults.length === 0 && selected !== null) {
    // sync in-render to avoid showing a stale selection frame
    setSelected(null);
  } else if (searchResults.length > 0 && selected == null) {
    setSelected(searchResults[0]);
  }

  // Imperative sync belongs in an effect.
  React.useEffect(() => {
    if (selected) scrollToSelected(selected);
  }, [selected]);

  return <ResultList results={searchResults} selected={selected} />;
}
```

**Example (Rules of Hooks)**
```jsx
function Conditional({enabled}) {
  React.useEffect(() => {}, []); // hooks must be unconditional
  const [x] = React.useState(0);
  if (!enabled) return <div />;
  return <div>{x}</div>;
}
```