---
title: Dataflow Cache Merge
description: When implementing or refactoring IR analyses/optimizations (derivation
  caches, constant propagation, mutation/aliasing lattices), treat cached facts as
  a *dataflow join*, not a last-writer-wins assignment.
repository: facebook/react#b12
label: Algorithms
language: TypeScript
comments_count: 6
repository_stars: 251896
---

When implementing or refactoring IR analyses/optimizations (derivation caches, constant propagation, mutation/aliasing lattices), treat cached facts as a *dataflow join*, not a last-writer-wins assignment.

Practical rules:
- Never overwrite an existing derivation entry for a place/lvalue with newly computed facts. Instead, merge/join the old and new information using the lattice/meet/join semantics you intend.
- Make join semantics explicit for every abstract kind/variant you introduce (e.g., new mutability kinds). If you add a kind, you must update merge/join logic and add tests for mixed-kind cases.
- Keep the analysis single-source-of-truth: prefer dataflow/derivations over type-based branching unless there is a strong, documented reason.
- Any transform that relies on CFG/value-block shape assumptions (e.g., rewriting value blocks/ternaries) must be guarded with invariants or focused fixtures that lock the intended structure.
- When using binding/scope information (to decide whether something is a true global vs shadowed), feed that into the analysis/derivation decisions so that merging remains semantically correct.

Example pattern (merge instead of overwrite):
```ts
// BAD: overwrites prior derived info
cache.set(placeId, {typeOfValue: newType, sourcesIds});

// GOOD: join with existing
const prev = cache.get(placeId);
if (prev == null) {
  cache.set(placeId, {typeOfValue: newType, sourcesIds});
} else {
  cache.set(placeId, {
    typeOfValue: joinValue(prev.typeOfValue, newType),
    sourcesIds: new Set([...prev.sourcesIds, ...sourcesIds]),
  });
}
```