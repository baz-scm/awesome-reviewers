---
title: Iterative Cache Correctness
description: When using a cache inside fixpoint/iterative analyses (or any dependency-walk
  that relies on cached facts), ensure the cache is updated in a dependency-safe order
  and never drops critical fields just because an entry doesn’t exist yet.
repository: facebook/react#b16
label: Caching
language: TypeScript
comments_count: 3
repository_stars: 251891
---

When using a cache inside fixpoint/iterative analyses (or any dependency-walk that relies on cached facts), ensure the cache is updated in a dependency-safe order and never drops critical fields just because an entry doesn’t exist yet.

Apply these rules:
- Don’t under-collect cache keys/sources: avoid overly specific guards (e.g., “named identifier only”) that can omit relevant provenance. If a heuristic might miss cases, leave a TODO and add a fixture that demonstrates the missed scenario.
- Record required cached fields even on first encounter: don’t conditionally add derivations only when the cache already has an entry; you may still need to initialize fields like `typeOfValue` so later passes can use them.
- Preserve dependency order across iterations: for producer nodes (e.g., PHIs/definitions), update the cache before consumer instructions in the same iteration. Be careful with when you take snapshots—snapshot timing should support the intended “previous iteration vs current iteration” semantics.

Example pattern (dependency-safe within each iteration):
```js
let isFirstPass = true;
do {
  // Snapshot “previous” cache state for fixpoint iteration semantics
  derivationCache.takeSnapshot();

  // First: record producers (e.g., PHIs/defs) so consumers can read cached facts
  for (const block of fn.body.blocks.values()) {
    recordPhiDerivations(block, derivationCache);
  }

  // Then: walk consumers/instructions
  for (const block of fn.body.blocks.values()) {
    recordInstructionDerivations(block, derivationCache);
  }

  isFirstPass = false;
} while (derivationCache.hasChanges);
```

These practices prevent subtle bugs where cached provenance/type information is missing due to overly narrow keying, gated updates, or incorrect snapshot/record ordering.