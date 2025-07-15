---
title: Type-safe null handling
description: "Use TypeScript's type system and modern JavaScript features to prevent\
  \ null reference errors. \n\n**TypeScript type safety:**\n- Prefer `never` over\
  \ `undefined` for properties that shouldn't have values"
repository: vercel/ai
label: Null Handling
language: TypeScript
comments_count: 6
repository_stars: 15590
---

Use TypeScript's type system and modern JavaScript features to prevent null reference errors. 

**TypeScript type safety:**
- Prefer `never` over `undefined` for properties that shouldn't have values
- Use `unknown` instead of `any` when working with data of uncertain structure
- Validate data with zod schemas instead of using type assertions (`as`)
- Use proper type narrowing with type guards

**Modern JavaScript null checks:**
- Use nullish coalescing (`??`) for default values:
```typescript
// Instead of this:
const citations = response.message.citations ? response.message.citations : [];

// Do this:
const citations = response.message.citations ?? [];
```

- Use optional chaining (`?.`) for accessing properties on potentially undefined objects:
```typescript
// Instead of this:
const contentType = requestClone.headers.get('content-type') || '';
if (contentType.startsWith('multipart/form-data')) { /*...*/ }

// Do this:
const contentType = requestClone.headers.get('content-type');
if (contentType?.startsWith('multipart/form-data')) { /*...*/ }
```

Following these patterns leads to more robust, self-documenting code and fewer runtime errors from unexpected null/undefined values.