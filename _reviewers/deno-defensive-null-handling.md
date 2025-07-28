---
title: defensive null handling
description: Use defensive programming patterns to prevent null-related issues before
  they occur. This includes creating safe object copies to prevent mutations, using
  explicit null/undefined checks, and initializing objects safely.
repository: denoland/deno
label: Null Handling
language: JavaScript
comments_count: 4
repository_stars: 103714
---

Use defensive programming patterns to prevent null-related issues before they occur. This includes creating safe object copies to prevent mutations, using explicit null/undefined checks, and initializing objects safely.

Key practices:
- Create defensive copies using spread syntax when you don't want to expose the underlying object: `{ ...originalObject }` instead of direct assignment
- Use explicit checks for empty values: `message.length === 0` instead of `message === ""`  
- Initialize objects with null prototype when appropriate: `{ __proto__: null }` to prevent prototype pollution
- Be explicit with nullish coalescing defaults: carefully consider whether `?? true` or `?? false` is the correct default

Example:
```javascript
// Good - defensive copy prevents mutation
ObjectAssign(internals, { core, nodeGlobals: { ...nodeGlobals } });

// Good - explicit length check
const formattedMessage = message.length === 0 ? "" : `${message} `;

// Good - null prototype prevents pollution
attributes = { __proto__: null };
```

This approach prevents null reference errors, unintended mutations, and makes null handling intentions explicit in the code.