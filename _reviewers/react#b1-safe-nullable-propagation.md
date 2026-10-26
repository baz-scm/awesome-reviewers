---
title: Safe Nullable Propagation
description: 'When dealing with `null`/`undefined` (or “disabled/off” states), never
  assume optional metadata exists or is stable.


  **Rules**

  1. **Propagate optional span/offset fields consistently**: if a node may omit `start`/`end`
  offsets, copy them from the original node when available; otherwise delete them
  (don’t leave stale values).'
repository: facebook/react#b1
label: Null Handling
language: TypeScript
comments_count: 5
repository_stars: 251878
---

When dealing with `null`/`undefined` (or “disabled/off” states), never assume optional metadata exists or is stable.

**Rules**
1. **Propagate optional span/offset fields consistently**: if a node may omit `start`/`end` offsets, copy them from the original node when available; otherwise delete them (don’t leave stale values).
2. **Never key identity off optional `loc.*` strings**: cache/map keys must be stable identifiers (e.g., `IdentifierId`, `InstructionId`, AST/HIR ids), not `loc.identifierName`/similar optional fields that may be missing and cause collisions.
3. **Rely on type narrowing**: after `if (x != null)`, use `x` directly—avoid `as` casts that defeat null safety.
4. **Filter “Off/disabled” early**: if a severity/flag can be `Off`, exclude it during aggregation/boolean logic so disabled details don’t affect outcomes.
5. **Be explicit with `?.` and `??`**: ensure the nullability you’re handling matches the value’s actual contract (the `??` fallback should only be relied on when the LHS can truly be nullish).

**Example**
```ts
// 1) Span/offset propagation
const applySourceOffsets = (node: t.Node): void => {
  if (node.loc == null) return;
  const source = sourceNodes.get(node.loc);
  if (!source) return;

  if (source.start === undefined) delete node.start;
  else node.start = source.start;

  if (source.end === undefined) delete node.end;
  else node.end = source.end;
};

// 2) Stable cache keys (NOT loc.identifierName)
const derivationCache = new Map<IdentifierId, Array<Place>>();

function getPlacesForIdentifier(id: IdentifierId): Array<Place> {
  const existing = derivationCache.get(id);
  if (existing) return existing;
  const computed: Array<Place> = /* compute */ [];
  derivationCache.set(id, computed);
  return computed;
}

// 3) No unsafe casts after narrowing
if (lvalue != null) {
  // use lvalue directly; don't cast
}

// 4) Exclude disabled/off details
function isError(details: Array<{severity: ErrorSeverity}>): boolean {
  return details.some(d => d.severity !== ErrorSeverity.Off);
}
```