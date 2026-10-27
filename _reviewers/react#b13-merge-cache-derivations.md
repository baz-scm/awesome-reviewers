---
title: Merge cache derivations
description: 'When maintaining a derivation/inference cache during multi-pass (fixpoint)
  analysis, treat the cache as the source of truth and update it conservatively:'
repository: facebook/react#b13
label: Caching
language: TypeScript
comments_count: 4
repository_stars: 251893
---

When maintaining a derivation/inference cache during multi-pass (fixpoint) analysis, treat the cache as the source of truth and update it conservatively:

- **Use merge semantics, not overwrite:** if an operand already has cached metadata, combine existing and newly derived `typeOfValue`/`sourcesIds` instead of replacing the entry.
- **Don’t block first enrichment:** avoid logic like “only record derivations when the cache already has the entry” unless you also guarantee `typeOfValue` (and any other required metadata) will be recorded on first sight.
- **Seed in dependency order:** ensure facts produced by **PHIs/SSA merges** are recorded before instructions that consume those values in subsequent/adjacent walks.
- **Avoid overly narrow cache keying:** don’t restrict cached source tracking to a narrow identifier category if it can omit cases; where guards are necessary, add a TODO and/or fixture covering the likely misses.

Example (merge instead of overwrite):
```ts
// BAD: overwrites earlier knowledge
context.derivationCache.addDerivationEntry(operand, sources, typeOfValue);

// BETTER: merge with existing entry if present
const existing = context.derivationCache.cache.get(operand.identifier.id);
if (existing) {
  const mergedSources = new Set([...existing.sourcesIds, ...sources]);
  const mergedType = joinValue(existing.typeOfValue, typeOfValue);
  context.derivationCache.cache.set(operand.identifier.id, {
    ...existing,
    sourcesIds: mergedSources,
    typeOfValue: mergedType,
  });
} else {
  context.derivationCache.addDerivationEntry(operand, sources, typeOfValue);
}
```

Applying these rules prevents cache inconsistency (lost sources/types), missed metadata on first encounter, and ordering-related gaps that can break fixpoint convergence.