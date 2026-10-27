---
title: Cache correctness and completeness
description: 'When building/using derivation caches, require two properties: (1) the
  cache captures all relevant sources (avoid overly restrictive heuristics like “only
  named identifiers”), and (2) the cache is populated in the correct dependency order
  before any code reads from it (especially across CFG block boundaries like PHIs).'
repository: facebook/react#b8
label: Caching
language: TypeScript
comments_count: 2
repository_stars: 251889
---

When building/using derivation caches, require two properties: (1) the cache captures all relevant sources (avoid overly restrictive heuristics like “only named identifiers”), and (2) the cache is populated in the correct dependency order before any code reads from it (especially across CFG block boundaries like PHIs).

Apply this rule:
- Completeness: If you derive cache entries from syntax/IR nodes, ensure your cached “sources” set reflects all value kinds that can flow into derivations—not just a subset guarded by checks. If there’s uncertainty, add a fixture/TODO to lock in expected behavior.
- Ordering/consistency: In multi-pass or iterative walks, seed/populate dependency information (e.g., PHI derivations) before traversing instructions that consume those derived values. If you introduce snapshots, place them so they don’t capture an incomplete state.

Example pattern (ordering):
```js
let isFirstPass = true;
do {
  // Seed derived values first
  for (const block of fn.body.blocks.values()) {
    recordPhiDerivations(block, context);
  }

  // Then read/record derivations from instructions
  for (const block of fn.body.blocks.values()) {
    for (const inst of block.instructions) {
      // safe to read context for phi-defined values now
      processInstruction(inst, context);
    }
  }

  context.derivationCache.takeSnapshot();
} while (!context.derivationCache.converged);
```

Example pattern (completeness):
```js
// Prefer a robust sourcesIds computation over restricting to named identifiers only
context.derivationCache.cache.set(valueId, {
  place: node,
  sourcesIds: computeAllRelevantSourcesIds(node), // not just node.identifier.id
});
```