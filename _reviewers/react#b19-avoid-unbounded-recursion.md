---
title: Avoid unbounded recursion
description: When traversing trees, linked chains, or listener lists whose depth/length
  is determined by runtime data (fiber trees, promise chains, async-node "previous"
  chains, listener lists), avoid recursive algorithms. Recursion depth is bounded
  by the call stack, so any sufficiently deep or long structure (large component trees,
  long promise chains, many listeners...
repository: facebook/react#b19
label: Algorithms
language: JavaScript
comments_count: 3
repository_stars: 251893
---

When traversing trees, linked chains, or listener lists whose depth/length is determined by runtime data (fiber trees, promise chains, async-node "previous" chains, listener lists), avoid recursive algorithms. Recursion depth is bounded by the call stack, so any sufficiently deep or long structure (large component trees, long promise chains, many listeners on one value) can cause a stack overflow in production. Prefer iterative traversal using an explicit loop (and, if needed, an explicit work stack) so the algorithm's space usage is controlled and doesn't grow with call-stack depth.

When converting a recursive function to iterative, preserve the traversal order, keep a pointer back to parent/root for backtracking, and make sure all exit conditions (including cycle/completion checks) are handled explicitly in the loop. For example, a recursive fiber search:

```js
function findByHostInstance(internals, fiber, hostInstance) {
  if (getHostInstanceForFiber(internals, fiber) === hostInstance) {
    return fiber;
  }
  const children = collectChildren(fiber);
  for (let i = 0; i < children.length; i++) {
    const found = findByHostInstance(internals, children[i], hostInstance);
    if (found != null) return found;
  }
  return null;
}
```

can be rewritten iteratively:

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
    if (current === root) {
      return null;
    }
    current = current.sibling;
  }
}
```

Similarly, for chained/linked state propagation (e.g. waking up chunk listeners or walking a "previous" pointer chain), replace "check status, then recurse" patterns with "check status, then loop": re-check the state in a `while` loop and dispatch to the appropriate handler directly, rather than calling the same function again on itself. This keeps the algorithm's complexity and stack usage proportional to the loop, not to recursion depth, and makes it robust against arbitrarily large inputs.