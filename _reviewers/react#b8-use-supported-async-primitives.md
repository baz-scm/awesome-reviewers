---
title: Use Supported Async Primitives
description: 'When implementing async/Suspense-like behavior and component control
  flow, keep React correctness guarantees: (1) never break the Rules of Hooks, (2)
  keep render pure (no unsafe state/ref writes), and (3) use the supported async primitive
  (`use()`) instead of Promise-throw patterns or unsupported Promise creation inside
  state initializers.'
repository: facebook/react#b8
label: React
language: JavaScript
comments_count: 7
repository_stars: 251889
---

When implementing async/Suspense-like behavior and component control flow, keep React correctness guarantees: (1) never break the Rules of Hooks, (2) keep render pure (no unsafe state/ref writes), and (3) use the supported async primitive (`use()`) instead of Promise-throw patterns or unsupported Promise creation inside state initializers.

Guidelines
- Rules of Hooks: never return early before all hooks in that component are called.
- Render purity: don’t mutate refs/state during render; use state/effects for updates.
- Async/Suspense behavior:
  - Prefer `use(promise)` (or other supported APIs) over “throwing a Promise” to trigger suspense.
  - Avoid creating Promises inside state initializers / `useMemo` when React explicitly doesn’t support that pattern.
- Side effects & imperative sync: if you must call an imperative API (e.g., scrolling), do it in `useEffect` with derived dependencies.

Example (safe hooks + supported async)
```js
function Gate({promise}) {
  // Hooks first (no early return before hooks)
  const value = React.use(promise); // supported async primitive

  // Render can branch freely after hooks
  if (value == null) return null;
  return <div>{value}</div>;
}

function ScrollOnSelection({selectedIndex}) {
  const listRef = React.useRef(null);

  React.useEffect(() => {
    if (listRef.current != null) {
      listRef.current.scrollToItem(selectedIndex, 'smart');
    }
  }, [selectedIndex]);

  return <div ref={listRef} />;
}
```