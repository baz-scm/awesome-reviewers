---
title: Iterative Traversal With Memoization
description: 'When implementing algorithms that traverse trees/graphs (Fibers, async
  node chains, hook trees), prefer iterative traversal over recursion unless depth
  is strictly bounded. Also treat cycle detection and memoization/visited maps as
  first-class algorithm steps: update memo/visited on all relevant exit paths, and
  define what each sentinel/return value means...'
repository: facebook/react#b7
label: Algorithms
language: JavaScript
comments_count: 5
repository_stars: 251888
---

When implementing algorithms that traverse trees/graphs (Fibers, async node chains, hook trees), prefer iterative traversal over recursion unless depth is strictly bounded. Also treat cycle detection and memoization/visited maps as first-class algorithm steps: update memo/visited on all relevant exit paths, and define what each sentinel/return value means (e.g., cycle vs abort/undefined).

Application rules:
1) Avoid recursion for potentially deep or unbounded structures
- If the structure can be long (e.g., linked “previous” pointers) or fan out (many listeners), recursion may overflow the call stack.
- Prefer an explicit loop that walks child/sibling/return pointers or an explicit stack.

Example (iterative tree walk instead of recursive search):
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

2) Make visited/memo updates complete and consistent
- If you use a `visited` map to prevent rework or handle cycles, ensure entries are written on every exit path (including “undefined”/early returns) so later traversal doesn’t lose required semantics.
- If cycle behavior depends on distinguishing “in progress” vs “cached result,” ensure your sentinel is integrated with the actual cycle/exit logic (don’t assume it changes behavior if the traversal is still effectively recursive/linear).

3) Validate cycle handling against real failure modes
- If you still see stack overflows, the issue is often traversal depth (long linear chains), not only undetected cycles—move the traversal to an iterative form (or restructure the traversal) rather than only tweaking cycle return values.