---
title: Null-safe metadata handling
description: 'Treat any nullable/optional compiler metadata (locations, identifiers,
  places, spans) as *explicitly absent* and handle it deterministically:


  - **Early-return on missing container objects**: if an entire node/location is `null/undefined`,
  stop instead of continuing with partially-defined data.'
repository: facebook/react#b11
label: Null Handling
language: TypeScript
comments_count: 5
repository_stars: 251894
---

Treat any nullable/optional compiler metadata (locations, identifiers, places, spans) as *explicitly absent* and handle it deterministically:

- **Early-return on missing container objects**: if an entire node/location is `null/undefined`, stop instead of continuing with partially-defined data.
- **Propagate span fields consistently**: when cloning/creating nodes from another representation, copy required optional span offsets (`start`/`end`) the same way `loc` is copied, so downstream span consumers don’t see missing offsets.
- **Use stable keys, not optional subfields**: don’t key maps by optional properties like `loc.identifierName` (which may be missing). Prefer stable IDs (e.g., `IdentifierId`) so “missing name” doesn’t collapse multiple distinct values.
- **Assert invariants instead of silently tolerating unexpected shapes**: if you’ve established that inputs are always from a known set, replace “continue on undefined” with `CompilerError.invariant(...)` / invariant-style checks.
- **Rely on type narrowing**: after `if (x != null)`, avoid unnecessary `as` casts—use the narrowed value directly.

Example pattern:
```ts
const applyOffsets = (node: t.Node): void => {
  if (node.loc == null) return;
  const source = sourceNodes.get(node.loc);
  if (source == null) return;

  if (source.start === undefined) delete node.start;
  else node.start = source.start;

  if (source.end === undefined) delete node.end;
  else node.end = source.end;
};

// When an internal assumption should always hold:
CompilerError.invariant(isNamedIdentifier(sourceMetadata.place), {
  reason: 'Compiler internal error: expected named place',
});

// When keying collections:
// Use IdentifierId (stable) instead of loc.identifierName (optional).
const byId = new Map<IdentifierId, Array<Place>>();
```

Applying these rules prevents null/undefined metadata bugs, keeps spans consistent across transformations, and makes failures explicit when an invariant is violated.