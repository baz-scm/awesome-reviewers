---
title: Explicit optional type declarations
description: Always explicitly declare optional types in interfaces and function parameters
  rather than relying on runtime checks or using `any`. This improves type safety,
  makes null/undefined handling requirements clear, and prevents runtime errors.
repository: getsentry/sentry
label: Null Handling
language: TSX
comments_count: 4
repository_stars: 41297
---

Always explicitly declare optional types in interfaces and function parameters rather than relying on runtime checks or using `any`. This improves type safety, makes null/undefined handling requirements clear, and prevents runtime errors.

Example:
```typescript
// ❌ Poor - Implicit optionality, uses any
interface Props {
  data: any;
  config: any;
}

// ✅ Good - Explicit optional types
interface Props {
  data: DataType;
  config?: ConfigType;  // Explicitly optional
  extraction?: Extraction; // Clearly shows optionality
}
```

Benefits:
- Makes null/undefined handling requirements clear at compile time
- Prevents runtime errors from unexpected undefined values
- Improves code maintainability by documenting expectations
- Forces conscious decisions about null handling
- Enables better IDE support and type checking

When implementing components or functions with optional parameters, ensure the types accurately reflect which values could be undefined. This creates a contract that makes null handling requirements obvious to consumers.