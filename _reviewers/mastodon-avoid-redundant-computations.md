---
title: avoid redundant computations
description: Identify and eliminate computations that are performed repeatedly when
  they could be executed once. This includes moving loop-invariant checks outside
  of loops and reducing callback overhead that creates unnecessary function declarations.
repository: mastodon/mastodon
label: Performance Optimization
language: JavaScript
comments_count: 2
repository_stars: 48691
---

Identify and eliminate computations that are performed repeatedly when they could be executed once. This includes moving loop-invariant checks outside of loops and reducing callback overhead that creates unnecessary function declarations.

Common patterns to optimize:
- **Loop invariants**: Move conditions that don't depend on individual loop items outside the loop
- **Repeated function calls**: Cache results of expensive operations that don't change
- **Callback overhead**: Minimize complex function declarations that cause GC churn

Example from file upload validation:
```javascript
// Before: checking upload limit for every file
filesArray.some(file => {
  // ... file-specific checks ...
  || (files.length + media.size + pending > maxMediaAttachments)  // This doesn't depend on individual file!
})

// After: check upload limit once before processing files
if (files.length + media.size + pending > maxMediaAttachments) {
  // handle error
  return;
}
// Then process individual files without redundant check
```

This optimization reduces computational overhead and improves performance, especially in scenarios with loops, callbacks, or frequently called functions.