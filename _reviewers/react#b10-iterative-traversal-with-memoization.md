---
title: Iterative traversal with memoization
description: When walking Fibers/trees/graphs (especially async graphs), don’t rely
  on recursion if the shape can be deep or linear; use iterative traversal with an
  explicit stack/loop. Combine this with correct visited/memoization updates to preserve
  semantics.
repository: facebook/react#b10
label: Algorithms
language: JavaScript
comments_count: 5
repository_stars: 251894
---

When walking Fibers/trees/graphs (especially async graphs), don’t rely on recursion if the shape can be deep or linear; use iterative traversal with an explicit stack/loop. Combine this with correct visited/memoization updates to preserve semantics.

Apply:
1) **Prefer iterative traversal** for DFS/BFS-style walks over Fiber/async-node trees/graphs to prevent stack overflows.
2) **If you maintain a visited map**, update it on *every* relevant exit path (including “undefined/abort-like” outcomes) *before* unwinding stack frames, so memoization/cycle/abort behavior stays consistent.
3) **Preserve invariants with traversal order**: if downstream code depends on stable indexes or ordering (e.g., flattened hook order), keep a deliberate traversal order and lock it with tests.
4) **Leverage structure facts**: if a node is known to be a leaf, handle it directly instead of invoking generic recursion that assumes non-leaf behavior.

Sketch (iterative DFS + visited):
```js
function findNode(root, getChildren, getKey, targetKey) {
  const visited = new Map(); // key -> result/marker
  const stack = [root];

  while (stack.length) {
    const node = stack.pop();
    const key = getKey(node);

    if (visited.has(key)) {
      // Return cached result / or handle in-progress markers consistently
      continue;
    }

    visited.set(key, true);

    if (key === targetKey) return node;

    const children = getChildren(node);
    for (let i = children.length - 1; i >= 0; i--) {
      stack.push(children[i]);
    }
  }

  return null;
}
```

Key standard: **deep traversal ⇒ iterative; memoization ⇒ consistent writes; ordering ⇒ invariant-preserving.**