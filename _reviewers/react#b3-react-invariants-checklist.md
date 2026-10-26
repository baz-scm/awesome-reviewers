---
title: React Invariants Checklist
description: 'When working on React components, tests, or related tooling, keep these
  invariants true:


  1) Preserve reconciliation identity

  - If you wrap built-ins (e.g. via `React.lazy`), ensure the reconciler sees the
  correct `elementType` for reconciliation. Don’t replace the wrapper identity with
  the inner built-in.'
repository: facebook/react#b3
label: React
language: JavaScript
comments_count: 5
repository_stars: 251883
---

When working on React components, tests, or related tooling, keep these invariants true:

1) Preserve reconciliation identity
- If you wrap built-ins (e.g. via `React.lazy`), ensure the reconciler sees the correct `elementType` for reconciliation. Don’t replace the wrapper identity with the inner built-in.

2) Use the supported suspense mechanism
- Prefer `use(promiseOrResource)` (and corresponding supported patterns) instead of throwing a raw Promise in new code/tests.

3) Never violate the Rules of Hooks
- Call hooks unconditionally at the top level of a component (or within a consistent control-flow path). Avoid early returns before hooks.

4) Don’t mutate during render to sync derived state
- If you need to synchronize an imperative action (e.g. scrolling a list) with derived state, do it in an effect, not by writing to refs/state during render.

Example patterns
- Hooks (no early return before hooks):
```js
function Example({shouldReturn}) {
  const [count, setCount] = React.useState(0);
  React.useEffect(() => setCount(1), []);
  if (shouldReturn) return null;
  return <div>{count}</div>;
}
```
- Suspense (prefer `use`):
```js
function Suspended({promise}) {
  const value = React.use(promise);
  return <div>{value}</div>;
}
```
- Imperative sync via effect:
```js
const listRef = React.useRef(null);
React.useEffect(() => {
  if (selectedId != null) {
    listRef.current?.scrollToItem(derivedIndex, 'smart');
  }
}, [selectedId, derivedIndex]);
```

Adopting this checklist prevents common correctness bugs: reconciliation failures with wrappers, suspense deprecations, hook static-flag/internal errors, and unsafe render-time updates that can cause stale or inconsistent UI.