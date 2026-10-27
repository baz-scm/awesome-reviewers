---
title: Safe setState patterns
description: Calling a state setter during render or inside an effect/callback can
  silently trigger infinite re-render loops or stale updates, so these patterns need
  to be caught holistically rather than only in the obvious, direct-call case.
repository: facebook/react#b20
label: React
language: TypeScript
comments_count: 4
repository_stars: 251895
---

Calling a state setter during render or inside an effect/callback can silently trigger infinite re-render loops or stale updates, so these patterns need to be caught holistically rather than only in the obvious, direct-call case.

- Never call a setter unconditionally during render (`setState(x)` in the component body). If you must derive state from props/other state, prefer computing it inline or memoizing it rather than storing it via `setState` during render, since it will re-trigger a render. A primitive, non-reactive value may be safe, but a reactive or object/array value is not — don't special-case this without also checking reactivity, not just "is it a primitive type".
- When calling a setter from inside `useEffect` (directly, through a nested function, or through a `useEffectEvent`), make sure the value passed isn't itself derived in a way that re-triggers the same effect, and audit for all the ways a value can flow from a ref or other instable source into the setter call — not only the direct top-level call, but through intermediate property loads, destructures, method calls, and nested helper functions. Prefer a generic "is this value derived from a ref/other instable source" propagation check that runs on every instruction's operands, rather than enumerating specific instruction kinds one by one, e.g.:

```js
const hasRefOperand = someOperand(value, operand => isDerivedFromRef(operand));
for (const lvalue of allLValues(instr)) {
  if (hasRefOperand) markDerivedFromRef(lvalue);
}
```

This should also catch cases like `setState(ref.current[index])`, `setState(getBoundingRect(ref))`, and `setState(ref.current.size * 10)`, not just a bare `setState(ref.current)`.
- When computing dependencies for `useEffect`/`useCallback`/`useMemo`, dependencies that come through compound expressions (array literals, spreads, method calls) must be traced back to their real source and surfaced with an accurate location so any "manual deps don't match actual deps" diagnostic points at something actionable.

Treat any state update that depends on an unstable source (render-time computation, refs, or another effect's output) as a potential infinite-loop or stale-state hazard, and validate it the same way regardless of how indirectly the value reaches the setter call.</description>
</invoke>
