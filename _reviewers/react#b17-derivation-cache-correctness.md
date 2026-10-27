---
title: Derivation cache correctness
description: 'When implementing caching (e.g., a derivation/fixpoint cache), treat
  cache entries as part of program semantics: ensure the cache is both complete and
  consistent across iterations.'
repository: facebook/react#b17
label: Caching
language: TypeScript
comments_count: 3
repository_stars: 251891
---

When implementing caching (e.g., a derivation/fixpoint cache), treat cache entries as part of program semantics: ensure the cache is both complete and consistent across iterations.

Apply this checklist:
- **Avoid overly narrow keys/filters:** Don’t only cache data for “named” identifiers if other operand shapes can participate in derivations. If you must narrow, add a **TODO + fixture** that demonstrates what could be missed.
- **Populate required metadata on first insert:** If the cache may not yet contain an operand entry, ensure the logic still records essential fields (e.g., `typeOfValue`) when adding the entry—not just on subsequent passes.
- **Respect producer→consumer ordering:** In iterative passes, record “producer” derivations (e.g., phi results) before walking instructions that consume them; snapshot/iteration changes must not allow consumers to observe incomplete cache state.

Example pattern (producer before consumer, first-insert metadata):
```ts
// producer: ensure phi-derived values exist in cache before use by downstream blocks
for (const block of fn.body.blocks.values()) {
  recordPhiDerivations(block, context); // populate cache for phi outputs
}

let changed;
do {
  context.derivationCache.takeSnapshot(); // align iteration boundary
  changed = false;

  for (const instr of block.instructions) {
    for (const operand of instr.operands) {
      if (isMutable(instr, operand)) {
        if (!context.derivationCache.cache.has(operand.identifier.id)) {
          // first insert must include type/origin metadata
          context.derivationCache.addDerivationEntry(
            operand,
            sources,
            typeOfValue,
          );
          changed = true;
        } else {
          // update existing entry as needed
          // ...
        }
      }
    }
  }
} while (changed);
```

Net effect: fewer “missing type/origin” bugs, fewer fixpoint/infinite-loop regressions caused by ordering changes, and more robust caching behavior across operand/identifier shapes.