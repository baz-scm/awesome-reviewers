---
title: Simplify and deduplicate code
description: Write concise, non-redundant code by eliminating unnecessary duplication
  and using simpler syntax where possible. This improves readability and maintainability.
repository: sveltejs/svelte
label: Code Style
language: TypeScript
comments_count: 4
repository_stars: 83580
---

Write concise, non-redundant code by eliminating unnecessary duplication and using simpler syntax where possible. This improves readability and maintainability.

Key practices:
- Remove redundant property definitions when extending interfaces or classes that already provide them
- Extract common logic into shared functions to prevent duplication across files  
- Use direct function references instead of arrow function wrappers when the signature matches
- Make exported types comprehensive to avoid forcing users to combine multiple types

Examples:
```typescript
// Instead of redundant property definitions:
export interface Derived<V = unknown> extends Value<V> {
  r_version: number; // ❌ Already defined in Value
}

// Use inheritance properly:
export interface Derived<V = unknown> extends Value<V> {
  // ✅ Only add new properties
}

// Instead of arrow function wrappers:
elements.forEach(element => detach(element)); // ❌

// Use direct function reference:
elements.forEach(detach); // ✅

// Make exported types complete:
export type ClassValue = string | ClassArray | ClassDictionary; // ✅
```