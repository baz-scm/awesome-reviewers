---
title: Iterative traversal algorithms
description: When traversing tree- or graph-like structures (fiber trees, async node
  chains, hook trees), prefer iterative algorithms over recursive ones. Recursive
  traversal can blow the call stack on deep or long linear chains (e.g. a `previous`-pointer
  chain with thousands of nodes), even when cycle detection is correct — the crash
  comes from recursion depth, not...
repository: facebook/react#b18
label: Algorithms
language: JavaScript
comments_count: 5
repository_stars: 251889
---

When traversing tree- or graph-like structures (fiber trees, async node chains, hook trees), prefer iterative algorithms over recursive ones. Recursive traversal can blow the call stack on deep or long linear chains (e.g. a `previous`-pointer chain with thousands of nodes), even when cycle detection is correct — the crash comes from recursion depth, not from the algorithm's logic. Walk the structure with an explicit stack or by using parent/sibling pointers instead:

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

When a traversal needs to compare or combine two structures, do it in a single pass (e.g. simultaneous DFS over both trees) rather than first flattening each into an intermediate array and comparing afterward — this avoids extra allocations and avoids subtle ordering bugs.

Also verify that memoization/visited-tracking stores every possible result, including `undefined`/`null` sentinels, so cached nodes aren't needlessly revisited or re-processed. For incrementally-built buffers/queues where items are drained from the front, pick a data structure that supports O(1) insertion and removal (e.g. a linked list) and actively clear processed entries — relying on an array with a "flushed pointer" that never advances, or shifting from the front, can leak memory or degrade to O(n) copies.