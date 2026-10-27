---
title: Explicit Null Handling
description: 'When code depends on nullable/optional fields, handle absence explicitly
  and safely:


  - Guard nullable inputs before use (e.g., `if (x == null) return;`).'
repository: facebook/react#b6
label: Null Handling
language: TypeScript
comments_count: 3
repository_stars: 251888
---

When code depends on nullable/optional fields, handle absence explicitly and safely:

- Guard nullable inputs before use (e.g., `if (x == null) return;`).
- When copying/cloning AST/HIR nodes, propagate optional location metadata consistently: if a source offset is `undefined`, explicitly remove the target field; otherwise assign it.
- Never use optional subfields as identity keys (e.g., don’t key caches by `loc.identifierName` if it may be missing). Use stable IDs or change the cache shape so missing optional metadata can’t collapse distinct entries.
- After checking `value != null`, rely on TypeScript narrowing instead of `as` casts.

Example (location offsets):
```ts
const applyOffsets = (target: {loc?: any; start?: number; end?: number}, sourceMap: Map<any, {start?: number; end?: number}>) => {
  if (target.loc == null) return;
  const source = sourceMap.get(target.loc);
  if (source == null) return;

  if (source.start === undefined) delete target.start;
  else target.start = source.start;

  if (source.end === undefined) delete target.end;
  else target.end = source.end;
};
```

Example (map keys):
```ts
// Bad: optional loc.identifierName can be missing and collapse entries.
// const key = place.loc?.identifierName;

// Good: use a stable identifier as the key (or map to arrays if multiple Places exist).
const cache: Map<IdentifierId, Place[]> = new Map();
```