---
title: Cache with Stable Inputs
description: When adding or updating memoization/caching logic, make the cache boundary
  depend only on inputs whose identity/stability you can guarantee, and memoize sub-values
  only when the consumer is pure with respect to those values.
repository: facebook/react#b12
label: Caching
language: Markdown
comments_count: 4
repository_stars: 251896
---

When adding or updating memoization/caching logic, make the cache boundary depend only on inputs whose identity/stability you can guarantee, and memoize sub-values only when the consumer is pure with respect to those values.

Rules:
1) Memoize independently only for pure consumers
- If the cached computation’s inputs are not mutated/consumed in a way that changes them, you can compute/memoize derived values separately.

Example (safe independent memoization when the callee doesn’t mutate its argument):
```js
const fn = fnFactory();
let t1;
if ($[0] !== b) {
  t1 = makeArray(b);
  $[0] = b;
  $[1] = t1;
} else {
  t1 = $[1];
}
const arr = t1;
fn(arr);
```

2) Treat ref-like values as unstable dependencies unless you can prove stability
- Don’t include a ref (or anything returned by a hook) as a memo dependency unless the codebase guarantees the ref identity is stable across renders.
- If `useCustomRef()` could return a different ref instance across renders, memo blocks must not assume ref identity stability.

3) Apply transitive memoization for custom macros
- If you introduce/modify a caching “macro” (e.g., a compiler/runtime helper that expands into multiple memoized expressions), ensure its arguments are transitively memoized so the cache boundary matches the macro’s expectations.

Applying these together prevents both over-caching (thrashing due to unstable dependencies) and under-caching (missing opportunities when inputs are safely independent).