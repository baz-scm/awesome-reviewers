---
title: Preserve Order, Optimize Traversals
description: When implementing tree/graph walking or streaming/collection logic, explicitly
  preserve the ordering invariant you depend on, and choose iteration/data-structure
  patterns that guarantee the intended time complexity.
repository: facebook/react#b6
label: Algorithms
language: JavaScript
comments_count: 4
repository_stars: 251888
---

When implementing tree/graph walking or streaming/collection logic, explicitly preserve the ordering invariant you depend on, and choose iteration/data-structure patterns that guarantee the intended time complexity.

Practical rules:
- Prefer iteration patterns with predictable complexity: avoid front-removal (`array.shift()`) in hot paths; instead track a drain index/pointer (O(1) per step overall).
- Preserve ordering invariants across transformations:
  - If the UI/data model requires “payload order,” ensure the produced sequence (e.g., FormData insertion order) matches the arrival order.
  - If you flatten a hook tree (or any nested structure) for index-based comparisons, keep a traversal order that keeps indexes aligned.
  - When merging debug/metadata from nested/reused elements, append vs prepend must match the required logical order.
- When traversing large trees, consider iterative traversal over recursion to reduce overhead and avoid stack depth issues.

Example: pointer-based drain that keeps insertion order and avoids O(N^2):
```js
const pendingFiles = []; // in arrival order
let flushedUpTo = 0;
function flush() {
  while (flushedUpTo < pendingFiles.length) {
    const pf = pendingFiles[flushedUpTo];
    if (!pf.complete) return; // preserve ordering invariant
    // resolve fields for pf here
    flushedUpTo++;
  }
}
```

Checklist to apply in code review:
- What ordering must be preserved (payload order, hook index order, logical metadata order)?
- Does the algorithm preserve it through flattening/merging?
- Are there any hidden O(N^2) behaviors (e.g., repeated front shifts)?
- Can traversal be iterative if the structure can be large?