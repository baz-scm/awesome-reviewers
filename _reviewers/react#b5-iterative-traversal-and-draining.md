---
title: Iterative Traversal and Draining
description: 'For deep/long-lived structures (trees, fiber graphs, linked async chains),
  avoid recursion and avoid complexity-worsening buffer operations.


  **Rules**'
repository: facebook/react#b5
label: Algorithms
language: JavaScript
comments_count: 3
repository_stars: 251886
---

For deep/long-lived structures (trees, fiber graphs, linked async chains), avoid recursion and avoid complexity-worsening buffer operations.

**Rules**
1. **Prefer iterative traversal** for tree/graph/chain walks when depth can be large.
   - Use an explicit loop (and/or manual stack) to prevent stack overflows.
2. **Keep traversal complexity predictable** (typically O(N) time / O(1)–O(H) extra space).
3. **When draining queued items, don’t use `shift()`/front-removal** in arrays.
   - Use a moving index pointer (O(N) total drain).
   - If you need frequent removals of arbitrary pending entries, consider a linked list or other structure that supports O(1) removals.
4. **Ensure termination cleanup**: if progress depends on “the last pending item,” make sure earlier drained state can’t leak if that last item never completes.

**Example patterns**
- Iterative tree walk (conceptual adaptation of the fiber suggestion):
```js
function findInTree(root, predicate) {
  let current = root;
  while (current !== null) {
    if (predicate(current)) return current;
    if (current.child !== null) {
      current = current.child;
      continue;
    }
    while (current !== root && current.sibling === null) {
      current = current.return;
    }
    if (current === root) break;
    current = current.sibling;
  }
  return null;
}
```
- Pointer-based buffer drain (instead of `shift()`):
```js
const pending = [];
let drainedUpTo = 0;
function drain() {
  while (drainedUpTo < pending.length) {
    const item = pending[drainedUpTo];
    if (!item.complete) return;
    // process item
    drainedUpTo++;
  }
}
```

Applying this standard prevents stack overflows in recursive traversals and avoids accidental O(N^2) behavior from naive queue/buffer implementations.