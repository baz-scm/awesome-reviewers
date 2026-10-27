---
title: Iterative Traversal & Drain
description: When traversing trees/graphs or draining buffered streams, prefer *iterative,
  order-preserving* algorithms that are safe for deep structures and avoid quadratic-time
  operations.
repository: facebook/react#b15
label: Algorithms
language: JavaScript
comments_count: 5
repository_stars: 251891
---

When traversing trees/graphs or draining buffered streams, prefer *iterative, order-preserving* algorithms that are safe for deep structures and avoid quadratic-time operations.

**Rules**
1. **Avoid recursion for Fiber/graph walks that can be deep or long-lived.** Use an explicit loop (and an explicit pointer/stack if needed) to prevent stack overflows.
2. **Drain queues/buffers in O(N):** don’t repeatedly `shift()`/remove from the front. Instead, keep a `flushedUpTo` index (or similar) and advance it.
3. **Choose data structures based on removal/cleanup needs:** if elements may stay “pending” indefinitely, consider structures that make cleanup/removal predictable (e.g., linked list) rather than an array that may retain large prefixes forever.
4. **Preserve required ordering invariants when flattening/traversing:** if indices/order matter to external semantics, ensure your traversal/flattening order matches that contract.

**Example (iterative traversal replacing recursion)**
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

**Example (O(N) drain with pointer)**
```js
const pendingFiles = [];
let flushedUpTo = 0;

function flush() {
  while (flushedUpTo < pendingFiles.length) {
    const f = pendingFiles[flushedUpTo];
    if (!f.complete) return; // hold later items to preserve payload order
    // ...apply f's buffered fields...
    flushedUpTo++;
  }
}
```

Apply this standard to any logic that walks React-like structures, async node graphs, or stream/buffer formats—especially where correctness depends on stable ordering and performance depends on avoiding hidden O(N^2) behaviors.