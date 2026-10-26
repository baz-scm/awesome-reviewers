---
title: Merge Derivation Caches
description: When updating derivation/type metadata in a cache, never overwrite existing
  entries blindly. Instead, merge new observations into the existing cached entry
  so you don’t lose facts discovered in earlier blocks/passes.
repository: facebook/react#b2
label: Caching
language: TypeScript
comments_count: 3
repository_stars: 251882
---

When updating derivation/type metadata in a cache, never overwrite existing entries blindly. Instead, merge new observations into the existing cached entry so you don’t lose facts discovered in earlier blocks/passes.

Apply this especially to fixpoint/iterative validation flows:
- Populate prerequisite cache data before consuming it (e.g., record phi derivations before walking instructions that read phi results).
- Ensure your “what counts as a source” logic is robust (avoid narrow checks that skip valid sources); add TODOs/fixtures to cover suspected misses.
- For each cache entry update, use merge semantics:
  - Combine/union `sourcesIds`.
  - Combine `typeOfValue` with a deterministic join (e.g., if different non-ignored types are observed, widen to a combined state such as `fromPropsAndState`).

Example pattern (merge vs overwrite):
```ts
function mergeEntry(oldEntry: Entry, newSources: Set<Id>, newType: TypeOfValue): Entry {
  const mergedSources = new Set([...oldEntry.sourcesIds, ...newSources]);
  const mergedType = joinValue(oldEntry.typeOfValue, newType); // deterministic join
  return { ...oldEntry, sourcesIds: mergedSources, typeOfValue: mergedType };
}

const existing = context.derivationCache.cache.get(id);
if (existing === undefined) {
  context.derivationCache.addDerivationEntry(lvalue, sources, typeOfValue);
} else {
  context.derivationCache.cache.set(id, mergeEntry(existing, sources, typeOfValue));
}
```

This prevents correctness bugs caused by losing earlier derivation facts when processing order changes or when multiple instructions contribute information to the same cached value.