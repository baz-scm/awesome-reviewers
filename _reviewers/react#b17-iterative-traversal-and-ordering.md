---
title: Iterative Traversal and Ordering
description: When walking potentially large/deep graphs or trees (Fiber trees, linked
  async-node chains, hook trees), prefer iterative traversal over recursion to avoid
  stack overflows, and ensure the walk preserves any required ordering/invariants.
repository: facebook/react#b17
label: Algorithms
language: JavaScript
comments_count: 3
repository_stars: 251891
---

When walking potentially large/deep graphs or trees (Fiber trees, linked async-node chains, hook trees), prefer iterative traversal over recursion to avoid stack overflows, and ensure the walk preserves any required ordering/invariants.

Apply this as a standard:
1) If recursion depth could be unbounded (deep/linear chains, large component trees), refactor to an iterative traversal (explicit loop or explicit stack).
2) If the traversal feeds positional data (e.g., “hook index corresponds to React hooks order”), write down the required ordering and make the traversal/flattening match it—changing traversal order can silently break index semantics.
3) Treat “cycle detection” and “deep recursion” separately: if the failure mode is stack overflow from deep chains, iterative traversal is the primary fix; sentinels may not help.

Example: replace recursive Fiber search with an iterative walk (using existing links) while keeping the same “first match” semantics:

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

For flattening trees (e.g., hook subHooks), explicitly choose a traversal order and confirm that the resulting leaf sequence aligns with the invariant you depend on (such as stable primitive-hook indexing).