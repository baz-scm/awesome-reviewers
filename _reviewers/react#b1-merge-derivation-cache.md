---
title: Merge Derivation Cache
description: When implementing caches of derived compiler/runtime facts (e.g., a “derivation
  cache”), treat cache updates as *accumulation* rather than replacement, and make
  iteration order explicit.
repository: facebook/react#b1
label: Caching
language: TypeScript
comments_count: 3
repository_stars: 251878
---

When implementing caches of derived compiler/runtime facts (e.g., a “derivation cache”), treat cache updates as *accumulation* rather than replacement, and make iteration order explicit.

**Rules**
1. **Merge, don’t overwrite:** If a cache entry already exists for an operand/value, combine the new derivation information with the existing entry (e.g., union `sourcesIds`, and compute/join `typeOfValue`). Avoid “last write wins” unless you can prove it’s correct.
2. **Record dependency-derived values before consuming them:** In multi-pass fixpoint loops, ensure you populate prerequisite derivations (e.g., phi-derived entries) before walking instructions that read those values. Make the ordering invariant explicit in code.
3. **Use snapshots/invalidation deliberately:** If the algorithm relies on convergence across passes, snapshot at the correct boundary and ensure each pass’s reads reflect the intended “before” state.
4. **Don’t narrow captured sources silently:** Don’t restrict cached source tracking to only special-case identifier kinds (e.g., “named identifiers”). If you do need a guard, add a TODO and a fixture that demonstrates what would otherwise be missed.

**Example (merge semantics sketch)**
```ts
// Instead of: context.derivationCache.cache.set(id, newEntry) // overwrites

const existing = context.derivationCache.cache.get(opId);
if (existing === undefined) {
  context.derivationCache.cache.set(opId, newEntry);
} else {
  context.derivationCache.cache.set(opId, {
    ...existing,
    sourcesIds: new Set([...existing.sourcesIds, ...newEntry.sourcesIds]),
    typeOfValue: joinValue(existing.typeOfValue, newEntry.typeOfValue),
  });
}
```

Applying these rules prevents subtle correctness bugs (missing/incorrect derivations) and improves cache robustness as the code evolves.