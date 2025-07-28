---
title: prefer efficient algorithms
description: Choose more efficient algorithmic approaches by leveraging built-in methods
  and APIs instead of implementing manual solutions. This includes using iterator
  methods over manual loops, direct comparisons over complex operations, and existing
  path traversal APIs over custom implementations.
repository: prettier/prettier
label: Algorithms
language: JavaScript
comments_count: 6
repository_stars: 50772
---

Choose more efficient algorithmic approaches by leveraging built-in methods and APIs instead of implementing manual solutions. This includes using iterator methods over manual loops, direct comparisons over complex operations, and existing path traversal APIs over custom implementations.

Key optimizations to apply:
- Use iterator methods like `.next().done` instead of manual for-loops with early returns
- Prefer direct comparisons (`a.offset - b.offset`) over complex multi-step operations
- Leverage existing APIs like `path.siblings`, `path.next`, `path.index` instead of manual array traversal with `findIndex()` and `find()`
- Consider O(1) operations and appropriate data structures for performance-critical code

Example transformations:
```javascript
// Instead of manual loop with early return
function isLeaf(node, options) {
  for (const _ of getChildren(node, options)) {
    return false;
  }
  return true;
}

// Use iterator method
function isLeaf(node, options) {
  return getChildren(node, options).next().done;
}

// Instead of complex string operations
if (!options.originalText.slice(locEnd(iNode), locStart(iNextNode)).includes(" "))

// Use direct comparison
if (locEnd(iNode) === locStart(iNextNode))

// Instead of manual array traversal
const elementIdx = elements.findIndex((v) => v == elementNode);
const nextNode = elements.find((e, i) => i > elementIdx && e !== null);

// Use path APIs
// path.siblings, path.next, path.index should be used
```

This approach reduces computational complexity, improves readability, and leverages well-tested library functions.