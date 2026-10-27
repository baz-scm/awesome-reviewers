---
title: Cache Derived Sets
description: Avoid accidental repeated work that increases algorithmic complexity,
  especially inside loops/filters. If you need a derived structure (e.g., `Set`) for
  membership checks, compute it once per scope and reuse it instead of reconstructing
  it for every element. When you add additional full-structure passes over large graphs/ASTs,
  measure and briefly document...
repository: facebook/react#b13
label: Performance Optimization
language: TypeScript
comments_count: 2
repository_stars: 251893
---

Avoid accidental repeated work that increases algorithmic complexity, especially inside loops/filters. If you need a derived structure (e.g., `Set`) for membership checks, compute it once per scope and reuse it instead of reconstructing it for every element. When you add additional full-structure passes over large graphs/ASTs, measure and briefly document the compile/runtime overhead so future changes can judge the tradeoff.

Example (eliminate O(n²) from rebuilding `Set` per element):

```ts
// Before: new Set(...) recreated for each filter element => O(n^2)
const rvalues = rvaluesUnfiltered.filter(
  v => !state.inScope(/*...*/) || state.identifiers.has(v.identifier.id),
);
// elsewhere in error path:
const undef = rvaluesUnfiltered.filter(v => new Set(rvalues).has(v));

// After: cache set once => O(n)
const rvaluesSet = new Set(rvalues);
const undef = rvaluesUnfiltered.filter(v => rvaluesSet.has(v));
```

Implementation standard:
- No `new Set(...)` (or similar expensive derivations) inside `map/filter/reduce` callbacks unless the input size is provably tiny.
- If extra full walks/passes are introduced, include a short comment describing the measured/expected overhead and the fact it was profiled/benchmarked.