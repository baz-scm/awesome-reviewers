---
title: Iterative Traversal, Ordered Drain
description: 'When implementing tree/graph traversals or queue-like buffering, design
  for (a) predictable complexity and (b) correct ordering semantics.


  **Standards**'
repository: facebook/react#b16
label: Algorithms
language: JavaScript
comments_count: 3
repository_stars: 251891
---

When implementing tree/graph traversals or queue-like buffering, design for (a) predictable complexity and (b) correct ordering semantics.

**Standards**
1. **Avoid recursion for potentially deep/linear structures.** If traversal could become long, prefer an **iterative walk** (e.g., follow `child`, then backtrack via `return`/`sibling`) rather than recursive DFS.
2. **Avoid O(N) queue operations.** Don’t repeatedly `shift()`/remove from the front of arrays. Use an **index/pointer** to drain in O(N), or a data structure with O(1) removal.
3. **Make traversal/flattening order explicit and match required indexing.** If consumer logic relies on positions (hook indices, insertion order, etc.), ensure the traversal/flattening strategy preserves that contract.
4. **Test worst cases:** deep chains, large buffers, and order-sensitive scenarios.

**Example (iterative tree walk + order-preserving traversal)**
```js
function findByHostInstance(root, hostInstance, getHostInstanceForNode) {
  let current = root;
  while (current !== null) {
    if (getHostInstanceForNode(current) === hostInstance) return current;

    if (current.child !== null) {
      current = current.child;
      continue;
    }

    while (current !== root && current.sibling === null) {
      current = current.return;
    }
    current = (current === root) ? null : current.sibling;
  }
  return null;
}

function drainInOrder(items) {
  // O(N) drain: advance pointer instead of shift()
  let i = 0;
  while (i < items.length) {
    const item = items[i];
    // ... process item ...
    i++;
  }
}
```

Applying this prevents stack overflows, removes accidental quadratic behavior from front-draining arrays, and ensures traversal-derived indexes/insertion order remain correct.