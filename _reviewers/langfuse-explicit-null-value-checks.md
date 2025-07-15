---
title: Explicit null value checks
description: Use explicit null/undefined checks instead of truthy/falsy checks when
  handling potentially null or undefined values. Relying on truthy/falsy checks can
  lead to bugs when dealing with valid falsy values like 0 or empty strings.
repository: langfuse/langfuse
label: Null Handling
language: TypeScript
comments_count: 4
repository_stars: 13574
---

Use explicit null/undefined checks instead of truthy/falsy checks when handling potentially null or undefined values. Relying on truthy/falsy checks can lead to bugs when dealing with valid falsy values like 0 or empty strings.

Bad:
```typescript
// May mishandle valid 0 values
if (curr.outputCost) {
  total = total.plus(curr.outputCost);
}

// Could yield "undefined" string
const username = String(env.USERNAME);
```

Good:
```typescript
// Explicitly checks for null/undefined
if (curr.outputCost != null) {
  total = total.plus(curr.outputCost);
}

// Uses nullish coalescing for default
const username = env.USERNAME ?? "default";
```

When parsing JSON or handling unknown data:
1. Use explicit type checks (typeof, instanceof)
2. Consider using the nullish coalescing operator (??) for defaults
3. Validate object structures after parsing
4. Be especially careful with numeric values where 0 is valid