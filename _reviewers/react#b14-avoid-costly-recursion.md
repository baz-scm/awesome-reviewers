---
title: Avoid costly recursion
description: When code can process large or adversarial shapes (many references, listeners,
  deep chains, large trees), ensure both **time complexity** and **stack depth** are
  bounded.
repository: facebook/react#b14
label: Algorithms
language: JavaScript
comments_count: 5
repository_stars: 251893
---

When code can process large or adversarial shapes (many references, listeners, deep chains, large trees), ensure both **time complexity** and **stack depth** are bounded.

Apply these rules:
- **No whole-structure rebuilds per event.** If an update is triggered repeatedly, avoid patterns like “clear and repopulate the entire Map/Set each assignment” (can degrade to O(n²)). Prefer incremental updates or rebuild once after collecting all changes.
- **Replace deep recursion with iterative traversal.** For tree/graph walks and long “previous”/linked chains, prefer an explicit loop (or explicit stack) so worst-case depth can’t overflow.
- **Avoid recursive wake/retry chains in hot paths.** In state/notification propagation, prefer checking “current state first, then act once” over recursively re-invoking the same function on many listeners.
- **Add stress tests for worst-case payload shapes** (e.g., Map/Set payloads with many deferred references; deep async-node chains) to catch O(n²) and stack-overflow regressions.

Example (iterative traversal skeleton):
```js
function findInFiberTree(root, match) {
  let current = root;
  while (current !== null) {
    if (match(current)) return current;
    if (current.child) {
      current = current.child;
      continue;
    }
    while (current && !current.sibling && current !== root) {
      current = current.return;
    }
    if (!current || current === root && !current.sibling) return null;
    current = current.sibling;
  }
  return null;
}
```

This standard prevents both performance blowups (O(n²) style) and runtime crashes (stack overflows) in algorithmically sensitive code paths.