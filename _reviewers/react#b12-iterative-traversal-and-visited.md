---
title: Iterative Traversal and Visited
description: When traversing trees/graphs (Fibers, async node graphs, listener/reference
  graphs), avoid recursion unless depth is provably bounded. Use iterative traversal
  (explicit loops/stack/queue) and maintain visited/memoization as a strict algorithmic
  invariant—set visited state at every exit/return boundary where semantics depend
  on “undefined vs null vs cycle vs...
repository: facebook/react#b12
label: Algorithms
language: JavaScript
comments_count: 5
repository_stars: 251896
---

When traversing trees/graphs (Fibers, async node graphs, listener/reference graphs), avoid recursion unless depth is provably bounded. Use iterative traversal (explicit loops/stack/queue) and maintain visited/memoization as a strict algorithmic invariant—set visited state at every exit/return boundary where semantics depend on “undefined vs null vs cycle vs in-progress”. Also prefer complexity-safe state draining (e.g., pointer/index draining instead of repeated shifts) and ensure early-exit paths don’t leave already-processed buffered state stranded.

Guidelines:
- **Prefer iterative traversal** for potentially deep/unbounded chains (e.g., long `previous` pointers, large Fiber trees, many listener callbacks). This prevents stack overflow and makes termination behavior clearer.
- **Make visited-map updates consistent**: if the algorithm distinguishes outcomes like `undefined` vs `null`, you must write the corresponding `visited` entry before unwinding (e.g., before stack pop / return) so memoization and abort/cycle semantics remain correct.
- **Handle “in progress” explicitly only if it changes returned semantics**; otherwise it won’t fix stack overflow caused by deep linear chains.
- **Use O(N) draining patterns**: advancing an index/pointer keeps total work linear. Ensure early exits still allow later cleanup (or choose a data structure like a linked list if you need constant-time removals).

Example (iterative tree walk instead of recursion):
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

Checklist for changes to traversal code:
- Does the structure have a worst-case depth that could grow large? If yes, make it iterative.
- Are all memoized results written on every relevant return path (including `undefined` cases)?
- Are cycle/in-progress states truly affecting return semantics?
- Are any queue/drain operations accidentally quadratic (e.g., repeated `shift`)?
- Do early exits leave buffered state inconsistent or leaked?