---
title: Cache Phase Ordering
description: When computing derivations using a cache during fixpoint/iterative analysis,
  treat cache writes and read timing as part of correctness—not an optimization.
repository: facebook/react#b10
label: Caching
language: TypeScript
comments_count: 2
repository_stars: 251894
---

When computing derivations using a cache during fixpoint/iterative analysis, treat cache writes and read timing as part of correctness—not an optimization.

Apply these rules:
1) **Don’t let `cache.has(...)` block required metadata.** If your semantics require tagging something (e.g., `typeOfValue` like `fromState`/`fromProps`), record it whenever needed—even if a derivation entry already exists.
   - Anti-pattern:
     - `if (cache.has(id)) return; // loses type tagging`
   - Preferred:
     - Split “presence of entry” from “presence of metadata you must write”.
2) **Preserve dataflow order across iterations.** Populate cache entries for *defining* nodes (e.g., Phi derivations) before you walk instructions that *consume* those definitions. Snapshot timing must align with that order so consumers never observe missing cache state.

Example pattern (self-contained):
```js
do {
  // Snapshot should happen at the start of the phase that consumes a stable cache view.
  derivationCache.takeSnapshot();

  // First: record derivations for definitions (Phi) that consumers will reference.
  for (const block of fn.body.blocks.values()) {
    recordPhiDerivations(block, derivationCache);
  }

  // Then: walk consumers and read cached metadata.
  for (const block of fn.body.blocks.values()) {
    for (const instr of block.instructions) {
      for (const operand of instr.operands) {
        if (isMutable(instr, operand)) {
          // Ensure required metadata is recorded even when the cache already has the entry.
          if (!derivationCache.hasEntry(operand.identifier.id)) {
            derivationCache.addDerivationEntry(operand, sources, typeOfValue);
          } else {
            derivationCache.ensureTypeTag(operand, typeOfValue);
          }
        }
      }
    }
  }
} while (derivationCache.hasChanges);
```

If you change phase ordering (e.g., moved calls during infinite-loop debugging), re-run an example where consumers depend on Phi/definition-derived cache entries—otherwise you may silently regress correctness.