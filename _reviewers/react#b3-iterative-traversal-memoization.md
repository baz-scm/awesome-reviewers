---
title: Iterative traversal & memoization
description: When traversing potentially deep trees/graphs (Fibers, async node graphs),
  prefer iterative algorithms with explicit state, and make memoization/visited updates
  consistent and semantically correct.
repository: facebook/react#b3
label: Algorithms
language: JavaScript
comments_count: 4
repository_stars: 251883
---

When traversing potentially deep trees/graphs (Fibers, async node graphs), prefer iterative algorithms with explicit state, and make memoization/visited updates consistent and semantically correct.

Apply these rules:
1) Prefer iteration over recursion for traversals that may be deep/linear
- If your walk can encounter long chains, recursion risks stack overflow.

Example (iterative tree walk):
```js
function findByHostInstance(internals, root, hostInstance) {
  let current = root;
  while (true) {
    if (getHostInstanceForFiber(internals, current) === hostInstance) {
      return current;
    }
    if (current.child !== null) {
      current = current.child;
      continue;
    }
    while (current !== root && current.sibling === null) {
      current = current.return;
    }
    if (current === root) return null;
    current = current.sibling;
  }
}
```

2) For memoized/visited traversals, update visited-map at the correct time
- Update `visited`/memo for every exit path before unwinding (e.g., before `stack.pop()`), so later re-visits preserve memoization.

3) Preserve distinct sentinel semantics
- Don’t collapse semantic differences in return values (e.g., `undefined` vs `null` can represent different behaviors like “abort semantics” vs “no I/O found”). If you introduce sentinels, ensure all code paths return the intended value.

4) Keep streaming/buffer operations complexity-safe
- When draining ordered buffers, avoid `shift()`; use an index/pointer so draining remains O(N), and plan cleanup if an entry can remain pending indefinitely.

Result: fewer stack overflows, correct cycle/abort behavior, and better worst-case performance characteristics.