---
title: Dataflow Merge Rules
description: 'When implementing compiler analyses/optimizations that compute facts
  over IR (e.g., “derived from X”, “typeOfValue”, mutation/alias effects), treat the
  problem as data-flow with lattice joins:'
repository: facebook/react#b14
label: Algorithms
language: TypeScript
comments_count: 3
repository_stars: 251893
---

When implementing compiler analyses/optimizations that compute facts over IR (e.g., “derived from X”, “typeOfValue”, mutation/alias effects), treat the problem as data-flow with lattice joins:

- **Never overwrite facts** for an identifier/place when a new derivation is discovered. Instead **merge/join** the existing fact with the new one (e.g., if `Mutable` joins with `ShallowMutable`, ensure the resulting kind follows the intended lattice rules).
- **Update iteratively to a fixpoint**: if facts can change based on control-flow (phi nodes, branches, generated temporaries), run multi-pass propagation until the cache stabilizes.
- **Propagate generically via IR operand iteration** (e.g., loop over `eachInstrValueOperand` / `eachInstrLvalue`) to avoid missing instruction kinds that carry the same derived data. Do the generic propagation step before any instruction-specific logic.
- **Guard correctness with fixtures** for edge cases that previously produced wrong results (false positives/negatives).

Example pattern (merge + generic propagation):
```ts
// Pseudocode inside a derivation pass
for (const instr of block.instructions) {
  // 1) Generic propagation: if any operand is derived-from-X, mark all output lvalues
  const hasDerivedOperand = some(eachInstrValueOperand(instr), op => isDerivedFromRef(op));
  if (hasDerivedOperand) {
    for (const lv of eachInstrLvalue(instr)) markDerived(lv);
  }

  // 2) For fact updates, always JOIN with prior value
  for (const lv of eachInstrLvalue(instr)) {
    const prev = cache.get(lv.id);
    const next = computeFact(instr, lv);
    cache.set(lv.id, joinFacts(prev, next)); // never overwrite with `next` directly
  }
}
```
Applying this standard prevents the two common failure modes seen in the discussions: (1) losing information by overwriting derivation entries, and (2) missing derived propagation because logic was too specific to a subset of instruction kinds.