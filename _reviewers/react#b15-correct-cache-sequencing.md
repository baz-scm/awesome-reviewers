---
title: Correct cache sequencing
description: When adding or modifying caching for derivations/analysis, treat correctness
  as a combination of (1) *what* gets cached and (2) *when* it becomes visible.
repository: facebook/react#b15
label: Caching
language: TypeScript
comments_count: 2
repository_stars: 251891
---

When adding or modifying caching for derivations/analysis, treat correctness as a combination of (1) *what* gets cached and (2) *when* it becomes visible.

Apply this standard:
1. **Cache inputs must be inclusive (no overly narrow identifier assumptions).** If your cache only records “named identifiers,” expand it to record all relevant source shapes, and add a fixture/TODO covering what could be missed by the prior narrow check.
2. **Cache updates must happen before dependent reads.** In control-flow traversals (e.g., blocks with phis feeding fallthrough instructions), record/update cached values at the point where subsequent instructions will read them. Avoid “debugging moves” that change ordering; add a regression case where a phi-produced value is referenced later.

Example pattern (ordering):
```js
// Ensure phi-derived values are recorded before walking instructions
for (const block of fn.body.blocks.values()) {
  recordPhiDerivations(block, context); // populate cache for downstream
  for (const inst of block.fallthroughInstructions()) {
    // inst may reference phi results (e.g., x@2)
    readFromCache(inst, context);
  }
}
```

Example pattern (robust cache inputs):
```js
// Don’t restrict sources to only 'named' identifiers
context.derivationCache.cache.set(paramKey, {
  place: param,
  sourcesIds: collectAllPossibleSourceIds(param), // not just named identifiers
  typeOfValue: /* ... */,
});
```

This prevents silent cache gaps (missing values) and missed dependencies (narrow source tracking), both of which can lead to incorrect validation results or infinite-loop risk during iterative passes.