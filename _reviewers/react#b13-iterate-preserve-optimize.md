---
title: Iterate, Preserve, Optimize
description: 'When implementing algorithms over trees/graphs/streams, ensure traversal
  safety, ordering correctness, and complexity/buffering efficiency.


  Apply this standard:'
repository: facebook/react#b13
label: Algorithms
language: JavaScript
comments_count: 4
repository_stars: 251893
---

When implementing algorithms over trees/graphs/streams, ensure traversal safety, ordering correctness, and complexity/buffering efficiency.

Apply this standard:
1) Prefer iterative traversal for potentially deep structures
- If recursion depth could exceed call-stack limits (e.g., long linear chains), use an iterative walk (explicit loop/stack/pointers) rather than recursive DFS.
- Ensure pruning/leaf special-casing doesn’t change required invariants.

2) Preserve required ordering / index semantics
- If the rest of the system depends on hook order, payload insertion order, or stable indexing, implement traversal/flattening so the mapping is deterministic.
- If you flatten trees, verify that the produced sequence matches the indexing rules used elsewhere; otherwise compare trees directly in lockstep to avoid index drift.

3) Make data movement linear-time and bounded
- Avoid patterns that repeatedly shift/splice from the front of arrays.
- Use a drain pointer (or equivalent) to keep total draining O(N).
- If the pipeline can stall (e.g., last pending item never completes), ensure already-emitted state can’t leak indefinitely; consider a structure that supports constant-time removal/cleanup.

4) Validate traversal correctness in cycle/abort scenarios
- If using sentinels for “in progress” vs “computed”, confirm behavior on real cyclic/awaited paths with tests; don’t assume the reported failure is due to cycles if the actual stack overflow comes from deep recursion.

Example (iterative tree search skeleton):
```js
function findByKey(root, getKey) {
  let current = root;
  while (true) {
    if (getKey(current) === target) return current;

    if (current.child) {
      current = current.child;
      continue;
    }

    while (current !== root && current.sibling == null) {
      current = current.parent;
    }
    if (current === root && current.sibling == null) return null;
    current = current.sibling;
  }
}
```

This reduces stack-overflow risk, preserves required semantics (ordering/indexing), and keeps runtime/memory behavior predictable.