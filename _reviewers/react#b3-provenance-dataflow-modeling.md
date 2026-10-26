---
title: Provenance Dataflow Modeling
description: When implementing or extending compiler validations/optimizations that
  depend on program behavior (effects, outlining safety, derived-from-X detection,
  mutation aliasing), require a sound *provenance/dataflow* model rather than ad-hoc
  instruction-kind checks.
repository: facebook/react#b3
label: Algorithms
language: TypeScript
comments_count: 5
repository_stars: 251883
---

When implementing or extending compiler validations/optimizations that depend on program behavior (effects, outlining safety, derived-from-X detection, mutation aliasing), require a sound *provenance/dataflow* model rather than ad-hoc instruction-kind checks.

Apply these rules:
1) **Represent abstract facts explicitly.** Use a dedicated cache/state (e.g., a derivation/provenance cache) that maps places/ids to metadata like “typeOfValue” and “sources”.
2) **Use a fixpoint when facts can change transitively.** If derivations depend on other derivations, compute to convergence (e.g., repeated passes with `snapshot()` until stable).
3) **Define and maintain the abstraction lattice.** If you add new abstract kinds (e.g., `ShallowMutable`), update: 
   - how kinds **join**
   - how specific operations **downgrade/upgrade** them
   - add fixtures for edge cases where joins produce the “wrong” kind without updated logic.
4) **Be precise about context/scope when validating outlining or captures.** Instruction kinds like `LoadContext`/`StoreContext` are not sufficient alone—compare against the function-expression’s explicit context array and ensure both loads and stores are handled.
5) **Propagate derived properties mechanically through IR.** Prefer a generic propagation helper that iterates over `eachInstructionOperand` / `eachInstructionLValue` and applies a consistent rule, instead of enumerating only a few instruction variants.

Example pattern (generic propagation idea):
```ts
const isDerivedFromRefId = new Set<IdentifierId>();

function markAllLvaluesDerivedFromRef(instr: Instruction) {
  const hasRefOperand = [...eachInstructionValueOperand(instr)].some(
    operand => isDerivedFromRefId.has(operand.identifier.id),
  );
  if (!hasRefOperand) return;
  for (const lvalue of eachInstructionLValue(instr)) {
    isDerivedFromRefId.add(lvalue.identifier.id);
  }
}
```

A change is considered compliant when it (a) updates/uses the provenance model, (b) correctly handles context/scope, (c) uses consistent propagation, and (d) includes/adjusts fixtures for the new abstract behavior (especially lattice join/downgrade cases).