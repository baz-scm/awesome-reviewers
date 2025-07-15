---
title: Use optional patterns
description: Choose the most appropriate pattern for handling potentially undefined
  or null values. When designing types, prefer optional properties (`?:`) over nullable
  types (`| null`) when a value is conceptually "not yet computed" rather than explicitly
  null.
repository: vitejs/vite
label: Null Handling
language: TypeScript
comments_count: 4
repository_stars: 74031
---

Choose the most appropriate pattern for handling potentially undefined or null values. When designing types, prefer optional properties (`?:`) over nullable types (`| null`) when a value is conceptually "not yet computed" rather than explicitly null.

For runtime null handling, use modern JavaScript features like nullish coalescing and optional chaining with idiomatic truthy checks:

```typescript
// Instead of nullable types with explicit initialization
class ModuleNode {
  isSelfAccepting: boolean | null = null;
}

// Prefer optional types
class ModuleNode {
  isSelfAccepting?: boolean;
}

// For runtime handling, use nullish coalescing
const listenOption = socket ?? { port, host: hostname };

// Use optional chaining with truthy checks
const rebase = pattern.match(/.*\/?node_modules\//)?.[0];
if (rebase) {
  // Do something with rebase
}
```

These patterns make code more concise, readable, and align with modern JavaScript idioms while maintaining type safety.