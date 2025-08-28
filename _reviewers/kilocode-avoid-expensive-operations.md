---
title: avoid expensive operations
description: Identify and mitigate costly operations that can significantly impact
  performance. This includes CPU-intensive processing, expensive I/O operations, and
  repeated function calls that involve file system access or complex computations.
repository: kilo-org/kilocode
label: Performance Optimization
language: TypeScript
comments_count: 2
repository_stars: 7302
---

Identify and mitigate costly operations that can significantly impact performance. This includes CPU-intensive processing, expensive I/O operations, and repeated function calls that involve file system access or complex computations.

When you encounter performance bottlenecks:
- Profile and measure the cost of operations before optimizing
- Consider disabling or replacing expensive features when they provide diminishing returns
- Batch expensive calls instead of making multiple separate calls
- Document performance decisions for future reference

Example of avoiding expensive operations:
```typescript
// Avoid: Multiple expensive calls
const { mode, apiConfiguration, language } = await this.getState()
const { experiments } = await this.getState() // Expensive I/O operation called twice

// Prefer: Single expensive call with full destructuring
const {
    mode,
    apiConfiguration, 
    language,
    experiments
} = await this.getState()

// Or disable expensive features when cost outweighs benefit:
// context = await this.addAST(context) // Disabled: uses too much CPU for Swift
```

Always weigh the performance cost against the actual benefit provided, especially for operations involving file I/O, network calls, or intensive computations.