---
title: Safe Null Handling
description: When a value is optional/nullable (e.g., `loc`, `start/end`, `loc.identifierName`,
  `lvalue`), don’t assume it exists. Either (a) preserve/copy the optional data consistently
  for downstream consumers, or (b) avoid using missing fields for logic such as cache
  keys. Also, use type narrowing after null checks instead of unsafe casts.
repository: facebook/react#b14
label: Null Handling
language: TypeScript
comments_count: 3
repository_stars: 251893
---

When a value is optional/nullable (e.g., `loc`, `start/end`, `loc.identifierName`, `lvalue`), don’t assume it exists. Either (a) preserve/copy the optional data consistently for downstream consumers, or (b) avoid using missing fields for logic such as cache keys. Also, use type narrowing after null checks instead of unsafe casts.

Guidelines:
- Optional node metadata: If you create/copy AST/IR nodes and `loc`-related fields are used by span consumers/backends, copy/propagate `start`/`end` when present; otherwise remove them or keep them unset consistently.
- Cache/map keys: Never key maps by a nullable/optional `loc.*` property (it may be absent and collapse multiple distinct items into the same bucket). Prefer stable identifiers or keys that can’t be `undefined`.
- Type narrowing: After `if (x != null)`, use `x` directly (no `as`) so TS can enforce null safety.

Example (safe key + narrowing):
```ts
// BAD: loc.identifierName may be missing -> different places collapse into one entry
// const key = place.loc?.identifierName;
// placesByName.set(key, ...);

// GOOD: use a stable IdentifierId (or another non-null key)
const placesById = new Map<IdentifierId, Array<Place>>();

function add(place: Place, id: IdentifierId | null | undefined) {
  if (id == null) return;
  const arr = placesById.get(id) ?? [];
  arr.push(place);
  placesById.set(id, arr);
}

// GOOD: narrowing avoids unsafe casts
function useLvalue(lvalue: Place | null | undefined) {
  if (lvalue != null) {
    // lvalue is non-null here
    doSomething(lvalue);
  }
}
```