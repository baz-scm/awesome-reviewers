---
title: Merge Dataflow Facts
description: When implementing optimizations/validations that compute or propagate
  metadata over an IR/graph (e.g., derivation caches, constant propagation, dependency
  inference), treat metadata updates as *joins* rather than replacements.
repository: facebook/react#b15
label: Algorithms
language: TypeScript
comments_count: 5
repository_stars: 251891
---

When implementing optimizations/validations that compute or propagate metadata over an IR/graph (e.g., derivation caches, constant propagation, dependency inference), treat metadata updates as *joins* rather than replacements.

**Standard**
1. **Never silently overwrite analysis facts**: if a fact for an identifier/place already exists, update it by merging/joining with the new info using a well-defined lattice/merge function.
2. **Define the merge**: document (and test) how combinations resolve (e.g., `fromProps` + `fromState` => `fromPropsAndState`).
3. **Guard transformation preconditions**: before rewriting control-flow/value-structure (e.g., turning a conditional/ternary into gotos or rewriting value-block expressions), verify the target’s structural shape matches what your transform assumes (and include all relevant instruction effects such as both Load/Store when detecting outer-scope references).

**Common bug pattern**
- Incorrect: replace an existing derivation entry with the current instruction’s type only.

```ts
// ❌ wrong: overwrites previous facts
cache.set(place, {typeOfValue: newType, sources: newSources});
```

- Correct: merge with what’s already known.

```ts
// ✅ correct: join/merge existing facts
const prev = cache.get(place);
const mergedType = mergeType(prev?.typeOfValue ?? 'ignored', newType);
const mergedSources = new Set([...(prev?.sources ?? []), ...newSources]);
cache.set(place, {typeOfValue: mergedType, sources: mergedSources});
```

Apply this to any multi-pass/dataflow-style logic (derivation caches, constant folding/propagation, dependency tracking, outer-scope capture detection) to avoid unsoundness from lost information and to keep optimizations stable as the IR evolves.