---
title: avoid quadratic complexity
description: When processing collections, be mindful of time complexity and avoid
  accidentally creating O(N²) algorithms, especially when simpler O(N) alternatives
  exist.
repository: prisma/prisma
label: Algorithms
language: TypeScript
comments_count: 3
repository_stars: 42967
---

When processing collections, be mindful of time complexity and avoid accidentally creating O(N²) algorithms, especially when simpler O(N) alternatives exist.

A common anti-pattern is using `reduce()` with object spread operations or similar approaches that create new objects in each iteration. This can lead to quadratic time complexity where linear complexity would suffice.

**Example of problematic O(N²) code:**
```javascript
const keysPerRow = rows.map((item) => 
  response.keys.reduce((acc, key) => ({ [key]: item[key], ...acc }), {})
)
```

**Improved O(N) alternative:**
```javascript
const keysPerRow = rows.map((item) => {
  const obj = {}
  for (const key of response.keys) {
    obj[key] = item[key]
  }
  return obj
})
```

Additionally, implement early returns for empty collections to avoid unnecessary processing:
```javascript
if (queries.length === 0) {
  return []
}
```

When choosing between implementation approaches, consider the computational complexity implications. Even micro-optimizations like using enums instead of strings can have measurable performance benefits in hot code paths, though the primary focus should be on avoiding algorithmic inefficiencies that scale poorly with input size.