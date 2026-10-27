---
title: Dataflow Merge Discipline
description: When implementing compiler analyses/optimizations (constant propagation,
  effect validation, derivation inference), drive correctness from dataflow/IR semantics—not
  type heuristics—and enforce *merge discipline*.
repository: facebook/react#b7
label: Algorithms
language: TypeScript
comments_count: 5
repository_stars: 251888
---

When implementing compiler analyses/optimizations (constant propagation, effect validation, derivation inference), drive correctness from dataflow/IR semantics—not type heuristics—and enforce *merge discipline*.

Apply these rules:
1) Dataflow-first: prefer deriving conclusions from tracked dataflow/derivation caches over mixed dataflow+typing checks.
2) Merge, don’t overwrite: if an entity (operand/lvalue/block) can be derived from multiple paths, combine results in the analysis lattice (e.g., join types, union sources, OR flags). Only replace when your lattice semantics say it’s equivalent.
   - Bad pattern (conceptually): `cache.set(id, newEntry)` where the prior entry must be joined.
   - Good pattern: `cache[id] = join(cache[id], newEntry)` (or union sources + join-kind).
3) Guard CFG/IR-shape assumptions: if your optimization assumes block structure (e.g., value-block fallthrough), add a runtime check before rewriting.
4) Use systematic traversal: when propagating facts from IR operands (e.g., “derived-from-ref”), traverse operands generically rather than enumerating many instruction cases.
5) Lock correctness with fixtures: when changing analysis logic, add at least one failing-but-shouldn’t-fixture to catch subtle mismatches.

Example (merge discipline sketch):
```ts
// Suppose derivationsCache maps id -> {typeOfValue, sourcesIds}
function addDerivation(id, newType, newSources) {
  const prev = derivationsCache.get(id);
  if (!prev) {
    derivationsCache.set(id, {typeOfValue: newType, sourcesIds: newSources});
    return;
  }

  derivationsCache.set(id, {
    typeOfValue: joinValue(prev.typeOfValue, newType),
    sourcesIds: new Set([...prev.sourcesIds, ...newSources]),
  });
}
```

These practices prevent common algorithmic bugs: false positives/negatives from incorrect assumptions, lost information due to overwrite, and brittle propagation logic that misses new IR shapes.