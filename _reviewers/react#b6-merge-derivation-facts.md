---
title: Merge Derivation Facts
description: 'When implementing data-flow analyses or optimization/validation passes
  that accumulate information (e.g., a derivationCache), treat analysis facts as elements
  of a lattice and **merge** them across all paths/uses. Concretely:'
repository: facebook/react#b6
label: Algorithms
language: TypeScript
comments_count: 3
repository_stars: 251888
---

When implementing data-flow analyses or optimization/validation passes that accumulate information (e.g., a derivationCache), treat analysis facts as elements of a lattice and **merge** them across all paths/uses. Concretely:

- **Never overwrite** an existing derivation entry for an operand/place when you discover additional evidence. Instead, **join** the previous and new facts (e.g., `typeOfValue = joinValue(old, new)`), and union their source-id sets.
- Make merge behavior explicit and centralized (a `joinValue(...)`/`merge(...)` helper), so new cases don’t accidentally bypass correct semantics.
- If you iterate to a fixpoint (snapshot/convergence), ensure the merge operation is monotonic so convergence is guaranteed.
- Pair the above with **fixture-based regression** for tricky CFG/value-block shapes that can invalidate rewrites (e.g., ternary/branch transformations that assume specific block structure).

Example pattern (merge instead of overwrite):
```ts
const existing = context.derivationCache.cache.get(id);
const incoming = {typeOfValue, sourcesIds};
if (existing === undefined) {
  context.derivationCache.addDerivationEntry(place, incoming.sourcesIds, incoming.typeOfValue);
} else {
  const joinedType = joinValue(existing.typeOfValue, incoming.typeOfValue);
  const joinedSources = new Set([...existing.sourcesIds, ...incoming.sourcesIds]);
  context.derivationCache.addDerivationEntry(place, joinedSources, joinedType);
}
```

This prevents false positives/negatives caused by dropping earlier evidence and is the foundation for reliable compiler algorithms that reason over control-flow.