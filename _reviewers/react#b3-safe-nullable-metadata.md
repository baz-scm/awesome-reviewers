---
title: Safe Nullable Metadata
description: When working with source locations, identifiers, or places, treat `loc`,
  nested fields, and derived strings as nullable/optional. Always (1) guard before
  dereferencing, (2) propagate metadata consistently (especially start/end ranges)
  without leaving partially-initialized nodes, and (3) use stable IDs for maps/caches
  instead of optional `loc.*` strings that...
repository: facebook/react#b3
label: Null Handling
language: TypeScript
comments_count: 4
repository_stars: 251883
---

When working with source locations, identifiers, or places, treat `loc`, nested fields, and derived strings as nullable/optional. Always (1) guard before dereferencing, (2) propagate metadata consistently (especially start/end ranges) without leaving partially-initialized nodes, and (3) use stable IDs for maps/caches instead of optional `loc.*` strings that can be absent.

Practical rules:
- Guard optional location data: `if (node.loc == null) return;` and only write `start/end` when the source provides them; otherwise delete/leave them unset.
- Preserve spans for all relevant nodes: if span consumers/backends expect `start/end` on a function node, ensure your node-construction utilities copy offsets from the original node (not just params/body).
- Don’t use nullable loc-derived strings as map keys: if `loc.identifierName` (or similar) might be missing, use a stable `IdentifierId`/ID in the key instead.
- Use type narrowing to avoid unsafe casts: after `if (x != null)`, use `x` directly (no `as`).

Example pattern:
```ts
const applyOffsets = (node: t.Node, sourceNodes: Map<any, {start?: number; end?: number}>) => {
  if (node.loc == null) return;
  const source = sourceNodes.get(node.loc);
  if (source == null) return;

  if (source.start === undefined) delete (node as any).start;
  else (node as any).start = source.start;

  if (source.end === undefined) delete (node as any).end;
  else (node as any).end = source.end;
};

// Prefer stable IDs over loc-derived strings:
const setStateCache: Map<IdentifierId, Array<Place>> = new Map();
// ... use IdentifierId as the map key, not loc.identifierName
```