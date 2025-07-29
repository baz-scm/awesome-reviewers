---
title: Use descriptive semantic names
description: Choose variable, function, and type names that clearly communicate their
  purpose and context. Prioritize readability and semantic meaning over brevity.
repository: remix-run/react-router
label: Naming Conventions
language: TypeScript
comments_count: 6
repository_stars: 55270
---

Choose variable, function, and type names that clearly communicate their purpose and context. Prioritize readability and semantic meaning over brevity.

Key principles:
- Use full descriptive names over abbreviations when clarity benefits (`State` instead of `S`, `handlerContext` instead of `context`)
- Choose readable prefixes over cryptic ones (`__ReactRouter_SerializesTo` instead of `$__RR_SerializesTo`)
- Align naming with existing patterns in the codebase (`navigationType` to match `useNavigationType` hook)
- Rename variables when their scope or purpose changes to maintain clarity

Example from codebase:
```typescript
// Before: Generic and unclear
let context = await loadRouteData(...)

// After: Specific and descriptive  
let handlerContext = await loadRouteData(...)

// Before: Cryptic prefix
export type SerializesTo<T> = {
  $__RR_SerializesTo?: [T];

// After: Clear, readable prefix
export type SerializesTo<T> = {
  __ReactRouter_SerializesTo?: [T];
```

This approach reduces cognitive load for developers and makes code self-documenting, especially important in large codebases where context switching is frequent.