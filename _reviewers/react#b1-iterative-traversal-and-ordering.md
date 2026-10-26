---
title: Iterative Traversal and Ordering
description: When implementing algorithms over trees/graphs (e.g., Fiber walks, async
  node traversals, hook-tree flattening, subtree toggles), prefer **iterative traversal**
  by default and make **ordering/index semantics explicit**. Also ensure any buffering/queue
  operations are **complexity-safe** (avoid accidentally introducing O(N²) behavior)
  and that “pending”...
repository: facebook/react#b1
label: Algorithms
language: JavaScript
comments_count: 6
repository_stars: 251878
---

When implementing algorithms over trees/graphs (e.g., Fiber walks, async node traversals, hook-tree flattening, subtree toggles), prefer **iterative traversal** by default and make **ordering/index semantics explicit**. Also ensure any buffering/queue operations are **complexity-safe** (avoid accidentally introducing O(N²) behavior) and that “pending” structures have a safe cleanup/exit path.

Practical rules:
- **Avoid recursion for potentially deep/linear structures.** If the depth can grow with input size (long await chains, large Fiber trees), use an explicit stack/loop to prevent stack overflow.
- **Only handle leaves specially when it’s guaranteed** (and document/verify you’re not relying on prior recursive behavior).
- **Preserve externally-defined ordering.** If indices are meaningful (e.g., hooks order) or if consumers expect outer-to-inner ordering, ensure your traversal/flattening/append-vs-prepend matches that contract.
- **Use complexity-appropriate buffering.** For queues over streaming data, prefer draining via an index pointer (O(N)) or a linked structure for O(1) removals; avoid shift-based front removal that can trigger repeated copying.

Example (iterative tree search instead of recursion):
```js
function findByHostInstance(internals, root, hostInstance) {
  let current = root;
  while (current !== null) {
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
    if (current === root && current.sibling === null) return null;
    current = current.sibling;
  }
  return null;
}
```

If you must recurse, add an explicit justification (e.g., maximum bounded depth) and add tests that would fail under deep inputs.