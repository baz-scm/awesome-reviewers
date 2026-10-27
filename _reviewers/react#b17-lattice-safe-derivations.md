---
title: Lattice-Safe Derivations
description: When implementing or refactoring data-flow/derivation analyses (constant
  propagation, effect validation, mutation aliasing, outlining eligibility), treat
  the analysis state as an abstract lattice and update it only via merge/join rules—never
  by overwriting.
repository: facebook/react#b17
label: Algorithms
language: TypeScript
comments_count: 4
repository_stars: 251891
---

When implementing or refactoring data-flow/derivation analyses (constant propagation, effect validation, mutation aliasing, outlining eligibility), treat the analysis state as an abstract lattice and update it only via merge/join rules—never by overwriting.

Practical rules:
1) **Derivation-cache updates must merge**
   - If an operand/value already has a derivation entry, incorporate the new evidence by *joining* types/kinds with the existing entry.
   - Do not replace the entry with the latest instruction’s `typeOfValue`/kind unless the merge operation explicitly says replacement is correct.

2) **Abstract-kind additions require full lattice updates**
   - When adding a new abstract kind (e.g. `ShallowMutable`), update all join/merge functions (e.g. `mergeValueKinds()`), and ensure interaction rules are encoded (e.g. `ShallowMutable | Mutable => Mutable`, while `ShallowMutable | x => ShallowMutable` when appropriate).

3) **Add fixtures for cross-kind interactions**
   - For each new join rule (or corrected merge behavior), add a small fixture that forces the analysis to combine kinds from different branches/paths.

Example failure pattern to avoid (conceptual):
```ts
// ❌ overwrites previously inferred info
derivationCache.set(id, {typeOfValue: newType});

// ✅ merges via join
const old = derivationCache.get(id);
derivationCache.set(id, {typeOfValue: joinValue(old?.typeOfValue, newType)});
```

This prevents silent unsoundness in multi-pass analyses where different instructions/blocks contribute partial evidence and the final result must reflect the combined (joined) abstraction rather than the last writer’s opinion.