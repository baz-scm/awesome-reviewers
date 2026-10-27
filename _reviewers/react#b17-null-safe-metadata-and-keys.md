---
title: Null-safe metadata and keys
description: 'When working with optional metadata (e.g., `node.loc`, `loc.identifierName`,
  `start/end` spans), treat missing values as first-class:

  - **Guard early**: `if (x == null) return/skip;`.'
repository: facebook/react#b17
label: Null Handling
language: TypeScript
comments_count: 3
repository_stars: 251891
---

When working with optional metadata (e.g., `node.loc`, `loc.identifierName`, `start/end` spans), treat missing values as first-class:
- **Guard early**: `if (x == null) return/skip;`.
- **Conditionally set or remove derived fields**: if a source value is `undefined`, explicitly `delete` the derived field rather than leaving it stale.
- **Use stable map keys**: don’t rely on optional `loc.*` properties for grouping/lookup—if the property may be absent, use a safer key shape (e.g., an existing stable ID) or avoid mapping those entries.
- **Rely on type narrowing**: after `if (value != null)`/`if (node.loc != null)`, use `value` directly and avoid `as` casts.

Example (derived span offsets + null-safe keying):
```ts
const applyOffsets = (node: {loc?: any; start?: number; end?: number}, sourceNodes: Map<any, any>) => {
  if (node.loc == null) return;
  const source = sourceNodes.get(node.loc);
  if (source == null) return;

  // Keep consumers consistent: omit when missing
  node.start = source.start === undefined ? undefined : source.start;
  node.end = source.end === undefined ? undefined : source.end;
  if (source.start === undefined) delete node.start;
  if (source.end === undefined) delete node.end;
};

// Map key: avoid optional loc.* fields
// Instead of map.get(place.loc?.identifierName)
// prefer map keyed by a stable identifier already present in HIR.
```

This prevents inconsistent span/metadata behavior and avoids accidentally collapsing distinct cases due to missing optional fields.