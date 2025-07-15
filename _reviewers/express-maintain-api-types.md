---
title: Maintain API types
description: Ensure API type definitions accurately reflect current implementations.
  When maintaining TypeScript definitions for APIs, regularly audit them against the
  actual source code to prevent developers from using non-existent or deprecated features.
repository: expressjs/express
label: API
language: TypeScript
comments_count: 2
repository_stars: 67300
---

Ensure API type definitions accurately reflect current implementations. When maintaining TypeScript definitions for APIs, regularly audit them against the actual source code to prevent developers from using non-existent or deprecated features.

For API type definitions:
1. Remove outdated type declarations that no longer exist in the implementation
2. Add clear comments for deprecated features or known limitations
3. Document version changes that affect API types

Example:
```typescript
// INCORRECT: Keeping outdated type definitions
/**
 * This function no longer exists in Express 5.0+
 */
export function query(options: qs.IParseOptions): Handler;

// CORRECT: Properly documenting API changes
/**
 * @deprecated Removed in Express 5.0 (2014-11-06)
 * @see https://github.com/expressjs/express/blob/master/History.md#500-alpha1--2014-11-06
 */
// export function query(options: qs.IParseOptions): Handler;
```

Accurate type definitions prevent confusion, reduce runtime errors, and improve developer experience when working with your API.