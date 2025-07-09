---
title: Handle nulls with types
description: 'Enforce type safety by properly handling null and undefined values through
  TypeScript types and explicit checks. Avoid using non-null assertions (!) or type
  assertions (as any), and instead:'
repository: elie222/inbox-zero
label: Null Handling
language: TSX
comments_count: 6
repository_stars: 8267
---

Enforce type safety by properly handling null and undefined values through TypeScript types and explicit checks. Avoid using non-null assertions (!) or type assertions (as any), and instead:

1. Use union types with null/undefined:
```typescript
// Bad
function process(value: string!) {
  return value.length;
}

// Good
function process(value: string | null) {
  if (!value) return 0;
  return value.length;
}
```

2. Provide explicit defaults using nullish coalescing:
```typescript
// Bad
const count = data?.count || 0;  // '' and 0 are treated as false
const name = user?.name || "Anonymous";  // '' is treated as false

// Good
const count = data?.count ?? 0;  // only null/undefined trigger default
const name = user?.name ?? "Anonymous";
```

3. Use type guards for complex objects:
```typescript
// Bad
interface Response { data: any }
const result = (response as Response).data;

// Good
interface Response { data: string | null }
function isResponse(value: unknown): value is Response {
  return typeof value === 'object' && value !== null && 'data' in value;
}
const result = isResponse(response) ? response.data : null;
```

This approach prevents runtime errors, makes null handling explicit, and leverages TypeScript's type system for better safety.