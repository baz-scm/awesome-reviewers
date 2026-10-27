---
title: Null-safe metadata propagation
description: When working with nullable/optional compiler metadata (e.g., `loc`, `loc.start/end`,
  `init?.loc`, `cache.get(...)` results, `loc.identifierName`), make null-handling
  explicit and stable.
repository: facebook/react#b9
label: Null Handling
language: TypeScript
comments_count: 5
repository_stars: 251891
---

When working with nullable/optional compiler metadata (e.g., `loc`, `loc.start/end`, `init?.loc`, `cache.get(...)` results, `loc.identifierName`), make null-handling explicit and stable.

Apply this consistently:
1) Propagate or intentionally omit offsets
- If a node may require span consumers (`start`/`end`), copy offsets from the original source when available; otherwise delete the fields rather than leaving them partially unset.

```ts
const applyOffsets = (node: t.Node, source: {start?: number; end?: number} | undefined) => {
  if (!source) return;
  if (source.start === undefined) delete node.start;
  else node.start = source.start;

  if (source.end === undefined) delete node.end;
  else node.end = source.end;
};
```

2) Don’t key maps by optional nullable subfields
- Avoid using optional `loc.identifierName` (or similar nullable subfields) as a map key; it can be missing and collapse distinct values.
- Use stable identifiers as keys (e.g., `IdentifierId`/`Identifier`) and store values in `Map<StableId, Array<Place>>`.

3) Prefer invariants when existence is guaranteed
- If earlier logic guarantees a lookup result exists, replace permissive `?.`/`undefined` branches with an invariant/assert so assumptions don’t silently degrade behavior.

4) Narrow nullable variables instead of casting
- After `x != null`, use `x` directly (no `as`), so the type system enforces null safety.

Net effect: fewer missing-span bugs, fewer silent “undefined merges” in maps, and clearer assumptions about when values must exist.