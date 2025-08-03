---
title: Cache expensive computed values
description: 'Cache frequently accessed or computed values to avoid redundant calculations
  and property lookups. This applies to:

  1. Loop invariant values

  2. Expensive computations'
repository: microsoft/typescript
label: Performance Optimization
language: TypeScript
comments_count: 4
repository_stars: 105378
---

Cache frequently accessed or computed values to avoid redundant calculations and property lookups. This applies to:
1. Loop invariant values
2. Expensive computations
3. Repeated property access
4. Function call results

Example - Before:
```typescript
while (index < path.length) {
    // path.length accessed on every iteration
    if (path.indexOf(separator, index) !== -1) {
        // indexOf called multiple times
    }
}
```

Example - After:
```typescript
const pathLength = path.length; // Cache loop invariant
const separatorIndex = path.indexOf(separator, index); // Cache computation
while (index < pathLength) {
    if (separatorIndex !== -1) {
        // Use cached values
    }
}
```

This optimization is particularly important in performance-critical paths and loops. When implementing, consider:
- Caching loop invariants outside the loop
- Storing repeated computation results in local variables
- Caching property accesses that won't change during execution
- Using local variables for values accessed multiple times

The performance impact can be significant, especially when the cached values are used frequently or the computations are expensive.