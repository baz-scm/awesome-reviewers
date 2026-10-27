---
title: Avoid unbounded recursion
description: When traversing trees, linked chains, or listener lists whose depth/length
  can be influenced by external or user data (e.g., Fiber trees, async "previous"
  chains, promise listener lists), avoid recursive implementations — they risk stack
  overflows once the structure grows large enough, and such growth is often outside
  the code's control. Prefer an iterative...
repository: facebook/react#b20
label: Algorithms
language: JavaScript
comments_count: 3
repository_stars: 251895
---

When traversing trees, linked chains, or listener lists whose depth/length can be influenced by external or user data (e.g., Fiber trees, async "previous" chains, promise listener lists), avoid recursive implementations — they risk stack overflows once the structure grows large enough, and such growth is often outside the code's control. Prefer an iterative approach using explicit pointers, a manual stack/queue, or a loop that checks state before acting, instead of recursive calls.

For example, rather than recursively calling into a fiber-tree search:
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

Similarly, for chain-like structures (e.g., waking up chunk listeners, walking "previous" pointers in async sequences), check the current state first, and only perform the follow-up action without recursing back into the same function — convert tail-recursive patterns into loops. When a true recursive solution is unavoidable, explicitly justify why depth is bounded, or add a sentinel-based iterative rewrite before merging. This keeps traversal safe and predictable for inputs whose size isn't controlled by the implementation itself, and avoids subtle stack-overflow regressions caught only by real-world repros.