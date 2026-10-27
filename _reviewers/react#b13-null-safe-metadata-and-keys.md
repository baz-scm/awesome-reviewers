---
title: Null-safe metadata and keys
description: When working with nullable/optional fields (especially `loc`-derived
  metadata like names/offsets), never assume presence, and never let missing values
  silently collapse distinct cases.
repository: facebook/react#b13
label: Null Handling
language: TypeScript
comments_count: 4
repository_stars: 251893
---

When working with nullable/optional fields (especially `loc`-derived metadata like names/offsets), never assume presence, and never let missing values silently collapse distinct cases.

Apply these rules:
1) **Guard optional span fields**: If `node.loc` is missing, or `source.start/end` are `undefined`, explicitly skip or delete the corresponding offsets so downstream consumers don’t interpret stale/partial spans.
2) **Preserve required offsets during node creation**: When transforming AST/HIR nodes, ensure new nodes copy all span-relevant fields (`start`/`end`) or apply an offsets function consistently; copying only `loc` can break backend parity and span consumers.
3) **Use stable keys for maps**: Don’t key `Map` entries by nullable `loc` subfields (e.g., `loc.identifierName`)—missing names can cause unrelated entries to merge. Prefer structural identifiers (e.g., the actual `Identifier`/`IdentifierId`) as the map key.
4) **Back required assumptions with invariants**: If “all entries must be known” (e.g., all `sourcesIds` are expected to exist), enforce it with `CompilerError.invariant(...)` rather than relying on unchecked assumptions.
5) **Leverage type narrowing**: After `if (x != null)`, use `x` directly instead of `as` casts.

Example (stable map key + offset handling):
```ts
// Stable key: identifier, not loc.*
const byIdentifier = new Map<IdentifierId, Array<Place>>();

function applyOffsets(node: {loc?: any; start?: number; end?: number}, source?: {start?: number; end?: number}) {
  if (node.loc == null) return;
  if (source == null) return;

  if (source.start === undefined) delete node.start;
  else node.start = source.start;

  if (source.end === undefined) delete node.end;
  else node.end = source.end;
}

// After null check: no cast
if (lvalue != null) {
  temporaries.set(lvalId, { root: { kind: 'NamedLocal', value: {...lvalue} }, path: [] });
}
```