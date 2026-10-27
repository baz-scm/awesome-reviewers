---
title: Merge dataflow facts
description: When implementing compiler analyses/optimizations that record derivation/type/effect
  facts (e.g., caches, “is derived from …” sets, abstract value kinds), update that
  state using **merge/join semantics**, not overwrite, and traverse operands/lvalues
  **generically** to avoid missing propagation paths.
repository: facebook/react#b8
label: Algorithms
language: TypeScript
comments_count: 3
repository_stars: 251889
---

When implementing compiler analyses/optimizations that record derivation/type/effect facts (e.g., caches, “is derived from …” sets, abstract value kinds), update that state using **merge/join semantics**, not overwrite, and traverse operands/lvalues **generically** to avoid missing propagation paths.

**Standard**
1. **Merge, don’t overwrite:** If a fact already exists, combine it with the new information (e.g., union of sources; join of abstract types). Avoid statements like “replace the operand’s derivation entry” unless you’ve proven the overwrite is sound.
2. **Use join operations consistently:** When abstract kinds/types are introduced or combined, ensure your `join`/`mergeValueKinds` logic is closed under all combinations.
3. **Prefer generic traversal helpers:** Derive dependency/alias/ref-propagation from `eachInstructionOperand(...)` / `eachInstructionValueOperand(...)` / `eachInstructionLValue(...)` style utilities, rather than special-casing only a subset of instruction kinds.
4. **Iterate to a fixpoint when needed:** If the analysis depends on propagation through control-flow/phi nodes, run repeated passes until the cache reaches a stable snapshot.

**Pattern**
```ts
// Pseudocode
for (const block of fn.body.blocks.values()) {
  recordPhiDerivations(block);
  for (const instr of block.instructions) {
    for (const operand of eachInstructionOperand(instr)) {
      const existing = derivationCache.get(operand.identifier.id);
      const incoming = computeTypeAndSources(operand, instr);
      if (existing) {
        derivationCache.set(operand.identifier.id, {
          type: join(existing.type, incoming.type),
          sources: union(existing.sources, incoming.sources),
        });
      } else {
        derivationCache.set(operand.identifier.id, incoming);
      }
    }
  }
}
// Repeat until snapshot stable if new derivations can appear
```

**Why this matters**
These rules prevent common unsoundness: losing previously discovered sources/types (overwrite), missing propagation through other IR instructions (narrow enumeration), and stopping before convergence (no fixpoint).