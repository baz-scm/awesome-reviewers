---
title: Define Equality Semantics
description: Ensure algorithmic helpers that use data structures (e.g., deep equality,
  key intersections) have an explicit correctness contract and are implemented with
  runtime-compatible structures.
repository: colinhacks/zod
label: Algorithms
language: TypeScript
comments_count: 3
repository_stars: 42628
---

Ensure algorithmic helpers that use data structures (e.g., deep equality, key intersections) have an explicit correctness contract and are implemented with runtime-compatible structures.

- **For deep equality:** verify the algorithm enforces *all* required invariants (e.g., same keys present in both objects, not just equal lengths). Clearly decide whether special values follow native `===` semantics or “collection” semantics (e.g., treating `NaN` as equal like `Set`).
- **For intersections/maps/sets:** don’t assume `Set`/custom map types are available or supported across all target runtimes. Prefer native `Map` when broadly supported, or implement a fallback/intersection that avoids `Set` when legacy environments matter.

Example (avoid `Set` for key intersection):
```ts
// Compatible intersection without Set
function sharedKeys(a: Record<string, unknown>, b: Record<string, unknown>) {
  const out: string[] = [];
  for (const key in a) {
    if (Object.prototype.hasOwnProperty.call(b, key)) out.push(key);
  }
  return out;
}
```

Apply this by (1) writing down the intended semantics (especially for equality) and (2) choosing the simplest compatible data structure/approach for the supported JavaScript environments.