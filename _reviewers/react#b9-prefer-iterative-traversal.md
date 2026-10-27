---
title: Prefer iterative traversal
description: When traversing Fiber/hook/async node trees (unknown or large depth),
  avoid recursive DFS implementations that can overflow the stack. Use an explicit
  iterative walk (or explicit stack) and, for graphs, maintain correct memoization/visited
  semantics (update visited before returning at all exit points; distinguish “in progress”
  vs “done” if needed).
repository: facebook/react#b9
label: Algorithms
language: JavaScript
comments_count: 4
repository_stars: 251891
---

When traversing Fiber/hook/async node trees (unknown or large depth), avoid recursive DFS implementations that can overflow the stack. Use an explicit iterative walk (or explicit stack) and, for graphs, maintain correct memoization/visited semantics (update visited before returning at all exit points; distinguish “in progress” vs “done” if needed).

Example (iterative tree walk pattern):

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

Checklist:
- If traversal depth can be large/unknown, prefer iterative traversal.
- For graphs (not pure trees), keep a visited map; ensure all return paths update it consistently so memoization doesn’t change semantics.
- If flattening hierarchical data for comparison/indexing, lock the traversal order to the semantics you rely on (don’t “fix” recursion order without verifying index expectations).