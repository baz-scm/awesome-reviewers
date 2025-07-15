---
title: Minimize memory allocations
description: 'Choose methods and patterns that reduce unnecessary memory allocations
  and object creation to improve performance. When working with buffers, prefer direct
  methods like `Buffer.byteLength()` over approaches that create intermediate objects:'
repository: vitejs/vite
label: Performance Optimization
language: TypeScript
comments_count: 4
repository_stars: 74031
---

Choose methods and patterns that reduce unnecessary memory allocations and object creation to improve performance. When working with buffers, prefer direct methods like `Buffer.byteLength()` over approaches that create intermediate objects:

```javascript
// Less efficient - creates an unnecessary buffer object in memory
const size = Buffer.from(chunk.code).length;

// More efficient - calculates the byte length directly
const size = Buffer.byteLength(chunk.code);
```

When handling object operations, avoid deep cloning when only specific properties are needed. Use targeted cloning strategies based on the actual requirements:

```javascript
// Less efficient - may clone objects unnecessarily
function deepClone<T>(value: T): T {
  if (Array.isArray(value)) {
    return value.map((v) => deepClone(v)) as T;
  }
  if (isObject(value)) {
    const cloned: Record<string, any> = {};
    for (const key in value) {
      cloned[key] = deepClone(value[key]);
    }
    return cloned as T;
  }
  // Only use structuredClone for complex types that need it
  if (value instanceof RegExp) {
    return structuredClone(value);
  }
  return value as T;
}
```

Be mindful of expensive operations like `structuredClone()` which can significantly impact performance on basic primitives. Consider using specialized handling for different data types to optimize memory usage and processing time.