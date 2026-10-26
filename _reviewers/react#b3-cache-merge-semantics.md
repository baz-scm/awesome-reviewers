---
title: Cache Merge Semantics
description: When maintaining a derivation/metadata cache during multi-pass analysis,
  updates must be *merge-based* (not overwrite-based) and must respect *record-before-read*
  ordering across snapshot boundaries.
repository: facebook/react#b3
label: Caching
language: TypeScript
comments_count: 3
repository_stars: 251883
---

When maintaining a derivation/metadata cache during multi-pass analysis, updates must be *merge-based* (not overwrite-based) and must respect *record-before-read* ordering across snapshot boundaries.

Apply this:
- **Merge, don’t overwrite:** If a cache entry for an operand/lvalue already exists, combine its existing sources/type with the newly computed ones.
  ```ts
  // Bad: overwrites prior info accumulated earlier/passed
  cache.set(lvalueId, newEntry);

  // Good: merge with prior info
  const prev = cache.get(lvalueId);
  cache.set(lvalueId, prev ? mergeEntry(prev, newEntry) : newEntry);
  ```
- **Record before read:** Ensure you populate Phi/derivation entries (or any prerequisite cached data) *before* iterating instructions that depend on them.
  - If you run an iterative loop with `takeSnapshot()`/stability checks, place the snapshot and the record step so each pass sees the required cached state.
- **Widen cache coverage + test misses:** Avoid overly narrow shape predicates for what can become a cached “source.” Add a TODO/fixture for known missed patterns, then adjust cache logic to include additional source forms.

This prevents subtle correctness regressions where analysis results depend on traversal order or where earlier derivations are lost due to overwrite semantics.