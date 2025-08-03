---
title: Guard against undefined
description: Always protect against potential null or undefined values before attempting
  property access or method calls to prevent runtime errors. This applies especially
  to array access, method calls like `.some()` or `.length`, and property access on
  objects that might be null.
repository: microsoft/typescript
label: Null Handling
language: TypeScript
comments_count: 5
repository_stars: 105378
---

Always protect against potential null or undefined values before attempting property access or method calls to prevent runtime errors. This applies especially to array access, method calls like `.some()` or `.length`, and property access on objects that might be null.

**Bad practice:**
```typescript
// Might throw if entrypoints is undefined
if (some(entrypoints, e => project.toPath(e) === path)) { ... }

// Might throw "Cannot read property 'length' of undefined"
const length = text.length;

// Potential index out of bounds
while (sourceFile.statements[pos].end < statement.end) { ... }

// Creates keys with 'undefined' as string literal
const key = `${useOnlyExternalAliasing ? 0 : 1}|${firstRelevantLocation && getNodeId(firstRelevantLocation)}|${meaning}`;
```

**Good practice:**
```typescript
// Guard with logical AND
if (entrypoints && some(entrypoints, e => project.toPath(e) === path)) { ... }

// Use optional chaining
const length = text?.length;

// Check array bounds
while (pos < sourceFile.statements.length && sourceFile.statements[pos].end < statement.end) { ... }

// Provide safe fallback value
const key = `${useOnlyExternalAliasing ? 0 : 1}|${firstRelevantLocation ? getNodeId(firstRelevantLocation) : 0}|${meaning}`;
```

Modern TypeScript provides several ways to handle nullable values safely: optional chaining (`?.`), nullish coalescing (`??`), and traditional guards (`x !== undefined`). Choose the approach that makes your code most readable while ensuring runtime safety.