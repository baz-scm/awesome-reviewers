---
title: prefer async/await patterns
description: Convert promise chains to async/await syntax for better readability,
  error handling, and proper cleanup operation placement. Async functions automatically
  return promises, so avoid redundant Promise.resolve() calls or manual promise wrapping.
repository: discourse/discourse
label: Concurrency
language: JavaScript
comments_count: 2
repository_stars: 44898
---

Convert promise chains to async/await syntax for better readability, error handling, and proper cleanup operation placement. Async functions automatically return promises, so avoid redundant Promise.resolve() calls or manual promise wrapping.

Key benefits:
- Cleaner error handling with try/catch blocks
- Proper placement of finally blocks that wrap entire operations
- Elimination of unnecessary promise constructors

Example transformation:
```javascript
// Before: Complex promise chain with misplaced finally
destroy(deletedBy, opts) {
  return this.setDeletedState(deletedBy).then(() => {
    // operation
  }).finally(() => {
    // cleanup only applies to inner promise
  });
}

// After: Clean async/await with proper cleanup scope
async destroy(deletedBy, opts) {
  this.set("isDeleting", true);
  try {
    await this.setDeletedState(deletedBy);
    // operation
  } finally {
    // cleanup applies to entire operation
    this.set("isDeleting", false);
  }
}
```

Avoid returning Promise.resolve() from async functions as they already return promises automatically.