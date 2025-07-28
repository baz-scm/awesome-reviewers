---
title: explicit API design
description: Design APIs with explicit parameters, consistent return types, and clear
  interfaces to improve usability and maintainability. Avoid boolean flags in favor
  of option objects, ensure consistent return types across all code paths, and use
  proper TypeScript overloads for type safety.
repository: nuxt/nuxt
label: API
language: TypeScript
comments_count: 6
repository_stars: 57769
---

Design APIs with explicit parameters, consistent return types, and clear interfaces to improve usability and maintainability. Avoid boolean flags in favor of option objects, ensure consistent return types across all code paths, and use proper TypeScript overloads for type safety.

Key principles:
- Use option objects instead of boolean parameters for extensibility
- Provide consistent return types to avoid type juggling
- Omit optional properties when not present rather than including undefined values
- Use TypeScript overloads to provide type-safe API variants

Example of explicit parameter design:
```typescript
// Instead of boolean flags
const start = (force: boolean = true) => { ... }

// Use option objects for clarity and extensibility
const start = (options: { force?: boolean } = {}) => { ... }
```

Example of consistent return types:
```typescript
// Instead of conditional return types that require type juggling
export function useObserver(): { observe: ObserveFn } | undefined

// Provide consistent interface with noop fallback
export function useObserver(): { observe: ObserveFn }
```

Example of proper property omission:
```typescript
// Omit optional properties when not present
const result = {
  path: pathname,
  ...(search && { query: parseQuery(search) }),
  ...(hash && { hash })
}
```

This approach makes APIs more predictable, reduces the need for runtime type checking, and provides better developer experience through clear interfaces and consistent behavior.