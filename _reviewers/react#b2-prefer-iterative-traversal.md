---
title: Prefer iterative traversal
description: When walking trees/graphs or draining streaming buffers, avoid recursion
  if depth/length can be large or unbounded. Prefer iterative traversal/state-machine
  style, and design queues/buffers so drain/removal is predictable (avoid operations
  that turn streaming into O(N²)).
repository: facebook/react#b2
label: Algorithms
language: JavaScript
comments_count: 5
repository_stars: 251882
---

When walking trees/graphs or draining streaming buffers, avoid recursion if depth/length can be large or unbounded. Prefer iterative traversal/state-machine style, and design queues/buffers so drain/removal is predictable (avoid operations that turn streaming into O(N²)).

Do:
- Replace recursive tree/graph walks with an explicit loop + manual stack/parent/sibling navigation.
- For streaming queues, drain using an index/pointer (advance a cursor) rather than removing from the front.
- Use data structures that match required operations (e.g., linked list/constant-time removal if you truly need frequent removals).

Don’t:
- Use recursion as a “search loop” or retry mechanism when it could process long chains/listeners and trigger stack overflows.

Example (iterative tree walk):
```js
function findByHostInstanceIter(internals, root, hostInstance) {
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

Example (pointer-based drain):
```js
const pending = [];
let drained = 0;
function flush() {
  while (drained < pending.length) {
    const item = pending[drained];
    if (!item.complete) return;
    drained++;
  }
  // optional: if drained is large, truncate once
  if (drained > 1024) pending.splice(0, drained);
}
```