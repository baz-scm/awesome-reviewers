---
title: Merge Dataflow Derivations
description: When implementing compiler/static analyses that compute facts over an
  IR (derivations, mutability, “derived from X”, dependency validation), treat the
  analysis as data-flow over a lattice and update facts with merge semantics.
repository: facebook/react#b11
label: Algorithms
language: TypeScript
comments_count: 3
repository_stars: 251894
---

When implementing compiler/static analyses that compute facts over an IR (derivations, mutability, “derived from X”, dependency validation), treat the analysis as data-flow over a lattice and update facts with merge semantics.

**Standards**
1. **Use fixpoint iteration for derived facts**
   - Re-run the analysis until the derivation cache reaches a stable snapshot (e.g., `do { ... } while (cache.snapshot())`).
2. **Never overwrite derivation facts blindly**
   - If a cache entry already exists, combine the existing and new information via a deterministic merge/join function (e.g., `fromProps | fromState -> fromPropsAndState`).
   - This prevents order-dependent bugs and preserves soundness.
3. **Propagate generically over operands before specializing**
   - In each instruction, first scan all operands (and sometimes the instruction’s produced lvalues) to determine whether any operand is already known to be derived from the source (e.g., a ref).
   - Then apply instruction-specific logic. This avoids missing propagation cases that a large switch can’t cover.

**Example pattern (merge + fixpoint)**
```ts
// Pseudocode
let changed: boolean;
do {
  changed = false;
  for (const instr of fn.instructions) {
    // compute inferredTypeOfValue / derivedFlags from operands
    const newFact = inferFromOperands(instr);

    const oldFact = derivationCache.get(instr.lvalue);
    const merged = mergeFacts(oldFact, newFact); // e.g., join lattice
    if (merged !== oldFact) {
      derivationCache.set(instr.lvalue, merged);
      changed = true;
    }
  }
} while (changed);
```

**Why**
- Overwriting derivations breaks monotonicity assumptions and can make results depend on traversal order.
- Relying only on instruction-specific propagation leads to incomplete coverage and subtle missed cases.

**Practical checklist**
- Have a `merge/join` function for each fact type.
- Ensure cache updates are monotonic (facts only move “up” in the lattice).
- Add a generic operand-scan for propagation booleans/flags.
- Include fixtures for cases that require propagation through non-obvious instructions (e.g., derived-from-ref through property loads, destructures, indexing).