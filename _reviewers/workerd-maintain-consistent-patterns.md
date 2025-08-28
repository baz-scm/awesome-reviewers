---
title: maintain consistent patterns
description: Ensure consistent coding patterns and approaches are used throughout
  the codebase, even when multiple valid alternatives exist. This improves code readability,
  reduces cognitive load for developers, and makes the codebase easier to maintain.
repository: cloudflare/workerd
label: Code Style
language: TypeScript
comments_count: 6
repository_stars: 6989
---

Ensure consistent coding patterns and approaches are used throughout the codebase, even when multiple valid alternatives exist. This improves code readability, reduces cognitive load for developers, and makes the codebase easier to maintain.

Key areas to focus on:

1. **Object Creation Patterns**: Use the same approach for creating objects with null prototypes consistently across files. If `Object.create(null)` is used in some places, avoid mixing it with `{ __proto__: null }` unless there's a specific technical reason.

2. **Type Handling**: Maintain consistent approaches for TypeScript type assertions and const assertions. When `as const` provides better type precision, apply it consistently across similar object definitions.

3. **Code Organization**: Follow established patterns for organizing utility functions, global declarations, and shared logic. If similar functionality exists elsewhere, extract it to a shared location rather than duplicating the pattern.

4. **API Compatibility**: When implementing Node.js-compatible APIs, preserve the mutability characteristics of the original APIs even if immutability would be preferred from a design perspective.

Example from the discussions:
```typescript
// Instead of mixing patterns:
export const _cache = { __proto__: null };        // In one file
const other = Object.create(null);                // In another file

// Use consistent approach:
export const _cache = Object.create(null);        // Everywhere
const other = Object.create(null);                // Everywhere
```

Before introducing a new pattern, check if similar functionality already exists and follow the established approach. When there's no clear precedent, document the chosen pattern and apply it consistently across related code.