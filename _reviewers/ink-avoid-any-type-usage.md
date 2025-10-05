---
title: avoid `any` type usage
description: Replace `any` type annotations with more specific types to improve type
  safety and null handling. The `any` type disables TypeScript's type checking, including
  null safety checks, making code prone to runtime errors.
repository: vadimdemedes/ink
label: Null Handling
language: TSX
comments_count: 4
repository_stars: 31825
---

Replace `any` type annotations with more specific types to improve type safety and null handling. The `any` type disables TypeScript's type checking, including null safety checks, making code prone to runtime errors.

Use `unknown` as a safer alternative when the type is truly unknown, as it requires type checking before use. When possible, use specific types like `ReactNode`, interfaces, or union types that accurately describe the expected values.

Example progression from unsafe to safe typing:
```typescript
// Avoid: Disables all type checking
let resolve: (value?: any) => void;

// Better: Requires type checking before use  
let resolve: (value?: unknown) => void;

// Best: Use specific types when known
let resolve: (value?: void) => void;

// For React components, use specific types
readonly unstable__transformChildren?: (children: ReactNode) => ReactNode;
```

This approach prevents null reference errors by ensuring TypeScript can properly track nullable and undefined values through the type system.