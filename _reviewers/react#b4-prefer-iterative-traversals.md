---
title: Prefer Iterative Traversals
description: When traversing trees/graphs or processing long/streaming sequences,
  avoid recursion and “shift-style” draining. Use iterative traversal and complexity-aware
  data structures so the implementation stays O(N) and won’t stack overflow.
repository: facebook/react#b4
label: Algorithms
language: JavaScript
comments_count: 4
repository_stars: 251885
---

When traversing trees/graphs or processing long/streaming sequences, avoid recursion and “shift-style” draining. Use iterative traversal and complexity-aware data structures so the implementation stays O(N) and won’t stack overflow.

Apply this when:
- The structure can be deep or contains long linear chains (e.g., linked “previous” pointers, Fiber trees).
- You buffer items that may complete out-of-order or stall; you still must keep draining work O(N) and avoid unbounded retained state.

Practical rules:
1) Replace recursive tree/graph walks with an explicit loop/stack, unless depth is provably bounded.
2) For staged queues, avoid `Array#shift()`; drain using an index/pointer (O(N)).
3) If you need frequent removals while preserving arrival order, consider a linked list (or equivalent) to keep removals constant-time.

Example (iterative walk pattern):
```js
function findByHostInstance(internals, root, hostInstance) {
  let current = root;
  while (true) {
    if (getHostInstanceForFiber(internals, current) === hostInstance) return current;

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

Example (pointer-based draining):
```js
const pendingFiles = [];
let flushedUpTo = 0;
function flush() {
  while (flushedUpTo < pendingFiles.length) {
    const f = pendingFiles[flushedUpTo];
    if (!f.complete) return; // hold later work
    // ...consume f...
    flushedUpTo++;
  }
  // if needed under stalls, clear/cleanup earlier entries that are already flushed
}
```

Net effect: safer algorithms (no stack overflow), predictable performance (O(N)), and controlled memory retention under partial/slow completion.