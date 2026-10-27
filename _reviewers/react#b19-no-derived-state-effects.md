---
title: No derived state effects
description: Don't use `useEffect` + `setState` to compute a value that is already
  derivable from props, state, or a ref during render. This "derived state in an effect"
  pattern causes an extra, unnecessary render pass and is a common source of stale
  or inconsistent UI. Compute the value directly in the component body instead, wrapping
  expensive calculations in...
repository: facebook/react#b19
label: React
language: TypeScript
comments_count: 4
repository_stars: 251893
---

Don't use `useEffect` + `setState` to compute a value that is already derivable from props, state, or a ref during render. This "derived state in an effect" pattern causes an extra, unnecessary render pass and is a common source of stale or inconsistent UI. Compute the value directly in the component body instead, wrapping expensive calculations in `useMemo` if needed.

```js
// Avoid: deriving state from props/refs inside an effect
function Component({items}, ref) {
  const [total, setTotal] = useState(0);
  useEffect(() => {
    setTotal(items.length); // just props.items.length, no need for an effect
  }, [items]);

  useEffect(() => {
    setSize(ref.current.size * 10); // derived from a ref
  });
}

// Prefer: compute directly during render
function Component({items}, ref) {
  const total = items.length;
  const size = ref.current ? ref.current.size * 10 : 0;
}
```

When reviewing or tooling for this pattern, treat any value that flows from a ref (`ref.current`, property loads on it, destructuring, method calls on it, arithmetic on it, etc.) as "ref-derived," and flag `setState` calls that consume ref-derived or prop/state-derived values inside effects rather than render. Reserve effects for genuine side effects (subscriptions, imperative DOM/ref work, logging) — not for mirroring values that could be computed synchronously.