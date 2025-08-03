---
title: Optimize critical loops
description: When implementing algorithms with nested loops or recursive operations,
  carefully analyze the computational complexity and optimize the critical path. Pay
  attention to loop ordering, early termination conditions, and unnecessary recomputation.
repository: microsoft/typescript
label: Algorithms
language: TypeScript
comments_count: 8
repository_stars: 105378
---

When implementing algorithms with nested loops or recursive operations, carefully analyze the computational complexity and optimize the critical path. Pay attention to loop ordering, early termination conditions, and unnecessary recomputation.

In path normalization algorithms (discussion 111-112), avoid quadratic behavior by using tight single-pass loops instead of repeated string operations:

```typescript
// Before: Potentially quadratic with repeated string operations
function getNormalizedAbsolutePath(path: string) {
  // Repeatedly finds separators with indexOf
  const sepIndex = path.indexOf(directorySeparator, index + 1);
  const altSepIndex = path.indexOf(altDirectorySeparator, index + 1);
  // ...
}

// After: Linear complexity with a single pass
function getNormalizedAbsolutePath(path: string) {
  let index = 0;
  while (index < path.length) {
    const ch = path.charCodeAt(index);
    // Process each character once with early termination
    if (isAnyDirectorySeparator(ch)) {
      // Handle separator
    }
    index++;
  }
}
```

When working with array comparisons (discussions 110, 144), consider the computational complexity of your algorithm:
1. Avoid nested loops when a single pass will suffice
2. Use early termination when a condition can't possibly be met
3. Structure data to match access patterns (discussion 67-68)
4. When ordering matters, ensure your algorithm preserves the intended behavior

For recursive algorithms, apply similar principles to prevent stack overflows and excessive computation.