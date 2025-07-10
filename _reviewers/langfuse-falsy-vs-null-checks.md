---
title: Falsy vs null checks
description: Distinguish between falsy values (0, '', false, null, undefined) and
  null/undefined values in your code. Use explicit checks for null/undefined when
  you want to preserve other falsy values.
repository: langfuse/langfuse
label: Null Handling
language: TSX
comments_count: 7
repository_stars: 13574
---

Distinguish between falsy values (0, '', false, null, undefined) and null/undefined values in your code. Use explicit checks for null/undefined when you want to preserve other falsy values.

For absence checks, use:
```typescript
// Instead of !value (catches all falsy values including 0, '', false)
if (value === undefined || value === null) { /* or simply: value == null */ }
```

For providing defaults, use the nullish coalescing operator:
```typescript
// Instead of value || defaultValue (replaces all falsy values)
const result = value ?? defaultValue; // Only replaces null/undefined
```

For filtering collections, be specific about what you're filtering:
```typescript
// Instead of .filter(Boolean) (removes all falsy values)
array.filter(item => item != null); // Only removes null/undefined
```

When working with math operations on potentially empty collections:
```typescript
// Provide a default to avoid -Infinity/Infinity
Math.max(0, ...array.map(item => item.value));
```

For browser APIs and nested objects:
```typescript
// Check existence before accessing properties
const available = typeof window !== "undefined" && window.Feature?.isEnabled;
```