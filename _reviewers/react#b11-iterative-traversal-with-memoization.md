---
title: Iterative Traversal With Memoization
description: 'When implementing traversal/search over trees/graphs, treat correctness
  as an algorithmic invariant: (1) don’t rely on implicit recursion assumptions (e.g.,
  leaf-vs-non-leaf), (2) keep memoization/visited updates consistent on *all* exit
  paths, and (3) use iterative traversal when depth can be large/unknown to avoid
  stack overflow.'
repository: facebook/react#b11
label: Algorithms
language: JavaScript
comments_count: 4
repository_stars: 251894
---

When implementing traversal/search over trees/graphs, treat correctness as an algorithmic invariant: (1) don’t rely on implicit recursion assumptions (e.g., leaf-vs-non-leaf), (2) keep memoization/visited updates consistent on *all* exit paths, and (3) use iterative traversal when depth can be large/unknown to avoid stack overflow.

**Checklist**
- **Iterate if depth is unbounded:** prefer an explicit stack/queue over recursive DFS/BFS.
- **Update `visited`/memo on every return path:** if a branch can end with `undefined`/`null`/sentinel values, ensure you store the exact semantic result (don’t “skip” updates on some exits).
- **Make special states explicit:** if you need to distinguish “in progress” from a real cached value, use a dedicated marker and ensure it changes the returned semantic only when intended.
- **Handle leaves/terminal nodes explicitly:** if a node is always a leaf, don’t depend on traversal recursion to “do nothing”; handle it directly.

**Example (iterative search with consistent memoization):**
```js
const IN_PROGRESS = Symbol('inProgress');

function findNode(root, getChildren, getKey, targetKey) {
  const visited = new Map(); // key -> result/marker
  const stack = [root];

  while (stack.length) {
    const node = stack.pop();
    const key = getKey(node);

    if (visited.has(key)) {
      // Cycle/in-progress handling: return/skip only if it matches the semantic you need.
      if (visited.get(key) === IN_PROGRESS) continue;
      continue;
    }

    // Mark in progress (or mark “no result” after fully explored, depending on semantics).
    visited.set(key, IN_PROGRESS);

    if (key === targetKey) {
      visited.set(key, node); // cache the concrete result
      return node;
    }

    // Expand children iteratively.
    const children = getChildren(node);
    for (let i = 0; i < children.length; i++) stack.push(children[i]);

    // If you need to memoize “not found”, do it explicitly here (not via incidental returns).
    visited.set(key, null);
  }

  return null;
}
```
Applying this standard prevents the common failure modes seen in the discussions: missed memoization updates at “abort/undefined” exits, incorrect cycle semantics, and stack overflows from deep linear traversals.