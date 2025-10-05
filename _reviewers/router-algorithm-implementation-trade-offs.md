---
title: algorithm implementation trade-offs
description: When implementing algorithms, carefully evaluate trade-offs between built-in
  methods, custom implementations, and different algorithmic approaches. Consider
  factors like browser compatibility, performance characteristics, maintainability,
  and edge case handling.
repository: TanStack/router
label: Algorithms
language: TypeScript
comments_count: 3
repository_stars: 11590
---

When implementing algorithms, carefully evaluate trade-offs between built-in methods, custom implementations, and different algorithmic approaches. Consider factors like browser compatibility, performance characteristics, maintainability, and edge case handling.

Key considerations:
- **Compatibility vs. Performance**: Built-in methods may not be available in all target environments. For example, `Array.findLast()` requires Safari 15.4+, necessitating custom implementations for broader compatibility.
- **Data Structure Handling**: Choose appropriate data structures based on usage patterns. For FormData processing, always using arrays simplifies logic despite slight overhead, while conditional arrays add complexity but optimize common cases.
- **String Processing Approaches**: Consider regex vs. conditional logic based on complexity and performance needs. Regex may seem simpler but can introduce escaping issues and compilation overhead.

Example from the discussions:
```typescript
// Custom implementation for compatibility
export function findLast<T>(
  array: ReadonlyArray<T>,
  predicate: (item: T) => boolean,
): T | undefined {
  for (let i = array.length - 1; i >= 0; i--) {
    const item = array[i]!
    if (predicate(item)) return item
  }
  return undefined
}

// vs. built-in (when available)
array.findLast(predicate)
```

Document the reasoning behind algorithmic choices to help future maintainers understand the trade-offs made.