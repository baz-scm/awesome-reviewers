---
title: prefer efficient built-ins
description: When multiple built-in methods can accomplish the same algorithmic task,
  prefer the single comprehensive method over combining multiple operations. This
  reduces computational overhead, simplifies code logic, and often provides better
  performance characteristics.
repository: denoland/deno
label: Algorithms
language: TypeScript
comments_count: 2
repository_stars: 103714
---

When multiple built-in methods can accomplish the same algorithmic task, prefer the single comprehensive method over combining multiple operations. This reduces computational overhead, simplifies code logic, and often provides better performance characteristics.

For example, instead of combining separate property retrieval methods:
```ts
// Less efficient - two separate operations
let allProperties = [
  ...Object.getOwnPropertyNames(obj),
  ...Object.getOwnPropertySymbols(obj),
];

// More efficient - single comprehensive method
let allProperties = Reflect.ownKeys(obj);
```

Similarly, use direct comparison methods when they handle edge cases automatically:
```ts
// Manual edge case handling
return NumberIsNaN(a) && NumberIsNaN(b) || a === b;

// Built-in handles all cases efficiently
return Object.is(a, b);
```

This approach improves algorithmic efficiency by leveraging optimized native implementations and reduces the cognitive load of understanding complex conditional logic.