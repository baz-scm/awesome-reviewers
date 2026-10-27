---
title: Avoid setState for derived state
description: Don't use `setState` to compute or synchronize derived values during
  render or inside `useEffect`/`useEffectEvent`. Calling `setState` unconditionally
  during render can trigger infinite re-render loops; calling it inside an effect
  just to recompute a value that depends on existing props/state causes an extra,
  avoidable render pass and makes data flow harder...
repository: facebook/react#b18
label: React
language: TypeScript
comments_count: 3
repository_stars: 251889
---

Don't use `setState` to compute or synchronize derived values during render or inside `useEffect`/`useEffectEvent`. Calling `setState` unconditionally during render can trigger infinite re-render loops; calling it inside an effect just to recompute a value that depends on existing props/state causes an extra, avoidable render pass and makes data flow harder to reason about. This includes indirect cases, such as calling a `setState` setter from inside a helper function invoked within an effect, or from inside a `useEffectEvent`-wrapped callback — these are still effect-time state updates and carry the same risk.

Instead, derive the value directly during render, or memoize it with `useMemo`/`useCallback` so it recomputes only when its real dependencies change:

```jsx
// Avoid: deriving state via an effect
const [fullName, setFullName] = useState('');
useEffect(() => {
  setFullName(`${firstName} ${lastName}`);
}, [firstName, lastName]);

// Prefer: derive directly during render
const fullName = `${firstName} ${lastName}`;

// Or, if the computation is expensive:
const fullName = useMemo(() => `${firstName} ${lastName}`, [firstName, lastName]);
```

When reviewing code that calls a state setter inside an effect, trace through any intermediate function calls or event wrappers to confirm the setter isn't just mirroring a value that could instead be computed inline or memoized. If a setState call during render is unavoidable (e.g., a guarded early bail-out), ensure the argument is a stable, non-reactive primitive to prevent re-render loops, and document why the pattern is necessary.