---
title: Choose efficient algorithms
description: 'When implementing algorithms, prioritize efficiency in both time and
  space complexity. Consider these specific optimizations:


  1. **Use bitwise operations** for mathematical computations when appropriate. For
  random number generation in ranges, bitwise operations can be more efficient than
  arithmetic expressions:'
repository: cloudflare/workerd
label: Algorithms
language: TypeScript
comments_count: 3
repository_stars: 6989
---

When implementing algorithms, prioritize efficiency in both time and space complexity. Consider these specific optimizations:

1. **Use bitwise operations** for mathematical computations when appropriate. For random number generation in ranges, bitwise operations can be more efficient than arithmetic expressions:
```javascript
// Instead of: Math.floor(Math.random() * (65535 - 32768 + 1)) + 32768
// Use: Math.random() * 0x8000 | 0x8000
```

2. **Prefer iterative solutions** over recursive ones when the recursion depth could be problematic or when a simple loop would be more efficient and readable. Even if recursion is unlikely to cause issues, iterative approaches often have better performance characteristics and avoid potential stack overflow risks.

3. **Understand memory implications** of data structure operations. When working with TypedArrays, use `subarray()` to create views instead of `slice()` to create copies, unless you specifically need a copy. This avoids unnecessary memory allocation and copying:
```javascript
// For views (no copy): array.subarray(start, end)
// For copies (when needed): array.slice(start, end)
```

These optimizations become particularly important in performance-critical code paths, large datasets, or resource-constrained environments.