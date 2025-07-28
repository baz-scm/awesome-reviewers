---
title: API abstraction levels
description: Functions and utilities should operate at appropriate abstraction levels
  without being aware of higher-level concepts or implementation details. This prevents
  tight coupling and improves reusability and testability.
repository: prisma/prisma
label: API
language: TypeScript
comments_count: 3
repository_stars: 42967
---

Functions and utilities should operate at appropriate abstraction levels without being aware of higher-level concepts or implementation details. This prevents tight coupling and improves reusability and testability.

When designing APIs, ensure that:
- Utilities take abstract parameters rather than concrete types from higher layers
- Functions accept processed inputs instead of calling internal functions themselves  
- Conditional logic is abstracted into proper interfaces rather than scattered throughout classes

**Example:**
Instead of making a utility aware of a specific `Client` type:
```typescript
// ❌ Bad - utility knows about high-level Client concept
export function createCompositeProxy<T extends object>(client: Client, target: T, layers: CompositeProxyLayer[]): T {
  // ...
  getPrototypeOf: () => Object.getPrototypeOf(client._originalClient),
}
```

Use an abstract parameter that provides only what's needed:
```typescript  
// ✅ Good - utility works with abstract prototype provider
export function createCompositeProxy<T extends object>(prototypeProvider: {}, target: T, layers: CompositeProxyLayer[]): T {
  // ...
  getPrototypeOf: () => Object.getPrototypeOf(prototypeProvider),
}
```

Similarly, abstract scattered conditionals into proper interfaces:
```typescript
// ❌ Bad - conditionals scattered throughout class
if (TARGET_BUILD_TYPE === 'rn') {
  // React Native specific logic
}

// ✅ Good - abstracted into library interface
const library = await libraryLoader.load()
await library.startTransaction(options)
```

This approach makes code more modular, testable, and maintainable by ensuring each component operates at its appropriate level of abstraction.