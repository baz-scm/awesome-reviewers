---
title: Optimize common search paths
description: Implement dedicated fast paths for common search patterns while maintaining
  a complete fallback path for edge cases. This optimization pattern significantly
  improves performance for frequent operations while ensuring correctness for all
  scenarios.
repository: vuejs/core
label: Algorithms
language: TypeScript
comments_count: 4
repository_stars: 50769
---

Implement dedicated fast paths for common search patterns while maintaining a complete fallback path for edge cases. This optimization pattern significantly improves performance for frequent operations while ensuring correctness for all scenarios.

Key implementation guidelines:
1. Identify the most common usage patterns
2. Create type-specific or pattern-specific fast paths
3. Maintain a complete fallback path for edge cases
4. Consider adding configuration options for traversal depth

Example:
```js
function optimizedSearch(values, target) {
  // Fast path for primitive type comparisons
  if (typeof target === 'number' || typeof target === 'string') {
    return values.includes(target)
  }

  // Fast path for same-type objects
  if (values.some(v => typeof v === typeof target)) {
    return values.some(v => String(v) === String(target))
  }

  // Fallback path for complex comparisons
  return values.some(v => looseEqual(v, target))
}
```

This pattern is especially valuable in framework code where the same operations are performed frequently. The fast paths handle common cases efficiently while the fallback ensures correctness for all scenarios.