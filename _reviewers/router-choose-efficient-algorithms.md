---
title: Choose efficient algorithms
description: Prefer built-in methods and appropriate data structures over manual implementations
  to improve both performance and code readability. Consider the computational complexity
  and trade-offs of different approaches.
repository: TanStack/router
label: Algorithms
language: TSX
comments_count: 3
repository_stars: 11590
---

Prefer built-in methods and appropriate data structures over manual implementations to improve both performance and code readability. Consider the computational complexity and trade-offs of different approaches.

When processing collections, leverage optimized built-in methods instead of manual loops:

```typescript
// Instead of manual reduce loop
const allParams = matches()
  .flatMap((m) => m.params)
  .reduce((prev, curr) => {
    const keys = Object.keys(curr)
    for (const key of keys) {
      if (prev[key] === undefined) {
        prev[key] = curr[key]
      }
    }
    return prev
  }, {})

// Use built-in methods with appropriate ordering
const allParams = Object.assign(
  {},
  ...matches()
    .reverse()
    .flatMap((m) => m.params),
)
```

Choose data structures based on your specific use case requirements. For detecting property additions, consider the trade-offs: Proxy for plain objects, or redesign to use Array.push() or Map.set() which can be more easily intercepted.

Avoid expensive type operations that can impact development performance. Default generic type parameters to simple types (like `string`) rather than large unions when the constraint already provides the necessary flexibility.