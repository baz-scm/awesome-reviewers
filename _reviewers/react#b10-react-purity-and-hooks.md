---
title: React Purity And Hooks
description: Maintain React correctness by (1) preserving the Rules of Hooks, (2)
  keeping render free of unsafe state/ref mutations, and (3) synchronizing imperative
  UI actions with derived state using effects.
repository: facebook/react#b10
label: React
language: JavaScript
comments_count: 4
repository_stars: 251894
---

Maintain React correctness by (1) preserving the Rules of Hooks, (2) keeping render free of unsafe state/ref mutations, and (3) synchronizing imperative UI actions with derived state using effects.

**Standards**
- **No early return before hooks:** If a component renders conditionally, still ensure all hooks are called in the same order on every render.
- **Render stays pure:** Avoid mutating refs/state as a mechanism to detect prop changes during render. Prefer `useState`/`useMemo`/derived values, or move the sync into an effect.
- **Imperative work in effects:** If you must call an imperative API (e.g. `listRef.current.scrollToItem(...)`) based on derived selection/state, do it in `useEffect` with explicit dependencies and clear guards (e.g. “only when something is selected”).

**Example**
```js
function CommitList({selectedId, index}) {
  // Hooks are unconditional
  const listRef = React.useRef(null);

  // Derived + guarded imperative sync
  React.useEffect(() => {
    if (selectedId == null) return;
    if (listRef.current == null) return;
    listRef.current.scrollToItem(index, 'smart');
  }, [selectedId, index]);

  return <FixedSizeList ref={listRef} />;
}

function ConditionalHooks({shouldUse}) {
  // Still call hooks unconditionally
  const [count, setCount] = React.useState(0);
  React.useEffect(() => {
    if (shouldUse) setCount(1);
  }, [shouldUse]);

  if (!shouldUse) return <div>No hooks used</div>;
  return <div>Count: {count}</div>;
}
```

Applying these rules prevents the class of bugs seen as internal hook/static-flag errors, render-time update hazards, and mismatches between derived React state and imperative UI behavior.