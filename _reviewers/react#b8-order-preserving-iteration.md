---
title: Order-Preserving Iteration
description: When operating on trees/graphs/streams, prefer algorithmic implementations
  that (a) cannot blow the call stack on deep/linear chains and (b) preserve the required
  semantic order while keeping complexity predictable.
repository: facebook/react#b8
label: Algorithms
language: JavaScript
comments_count: 5
repository_stars: 251889
---

When operating on trees/graphs/streams, prefer algorithmic implementations that (a) cannot blow the call stack on deep/linear chains and (b) preserve the required semantic order while keeping complexity predictable.

Guidelines:
- Use iterative traversal (explicit stacks or fiber-walking via child/sibling/return pointers) instead of recursion when depth is unbounded/unknown.
- When “draining” or consuming buffered items, avoid front-removal patterns that can turn into O(N^2) (e.g., repeatedly shifting). Use a read pointer (or a linked list if you truly need constant-time removals).
- Be explicit about ordering when flattening/combining structures (e.g., hook index semantics, debugInfo ordering, FormData insertion order). Tests should assert order, not just presence.
- If you introduce sentinels/cycle handling, verify the fix addresses the actual observed failure mode (e.g., stack overflow from long chains vs true cycle).

Example (iterative tree search replacing recursion):
```js
function findByHostInstance(internals, root, hostInstance) {
  let current = root;
  while (true) {
    if (getHostInstanceForFiber(internals, current) === hostInstance) return current;

    if (current.child !== null) {
      current = current.child;
      continue;
    }

    while (current !== root && current.sibling === null) current = current.return;
    if (current === root) return null;
    current = current.sibling;
  }
}
```

Example (order-preserving drain with a pointer instead of shifting):
```js
const pending = []; // arrival order
let i = 0;
function flush() {
  while (i < pending.length) {
    const item = pending[i];
    if (!item.complete) return; // preserve payload order
    // consume item
    i++;
  }
}
```