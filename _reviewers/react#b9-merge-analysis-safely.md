---
title: Merge Analysis Safely
description: When implementing IR validations/optimizations using multi-pass or cached
  data-flow (derivation, constant/ternary propagation, ref/alias propagation, etc.),
  treat correctness as a *join/merge* problem, not an overwrite problem, and ensure
  transformations only fire when structural invariants hold.
repository: facebook/react#b9
label: Algorithms
language: TypeScript
comments_count: 5
repository_stars: 251891
---

When implementing IR validations/optimizations using multi-pass or cached data-flow (derivation, constant/ternary propagation, ref/alias propagation, etc.), treat correctness as a *join/merge* problem, not an overwrite problem, and ensure transformations only fire when structural invariants hold.

**Coding standard**
1. **Never overwrite analysis facts blindly**: when an instruction/phi provides new metadata for an identifier, *merge* it with any existing entry (e.g., join value-kind/type classification + union source IDs).
2. **Use explicit “join” semantics**: if you introduce/propagate abstract kinds (e.g., mutability levels), update the join/merge rules globally so joins are consistent and monotonic.
3. **Guard rewrites with structural checks**: before converting control/value-flow (e.g., rewriting a terminal into a `goto`, or rewriting value blocks), verify the preconditions that make the rewrite valid (e.g., absence of nested/inner value-block shapes).
4. **Prefer operand-driven propagation over special-casing**: when tracking whether values/lvalues are derived from a property (like “derived from ref”), implement a generic pass like “inspect all operands; if any operand matches, mark all produced lvalues,” then handle only truly exceptional cases.
5. **Context/scope correctness is mandatory**: when deciding whether an inner function can be outlined or whether a symbol/identifier is truly global, compare against the *function’s tracked context* (and include all relevant load/store instruction forms).
6. **Require targeted fixtures for each edge**: every time you add a join rule, guard, or propagation behavior, add a failing fixture that would regress the prior incorrect behavior.

**Example (generic propagation pattern)**
```ts
for (const instr of block.instructions) {
  const operands = eachInstructionValueOperand(instr);
  const hasDerived = Iterable_some(operands, op => isDerivedFromRef(op));
  if (hasDerived) {
    for (const lvalue of eachInstructionLValue(instr)) {
      markIsDerivedFromRef(lvalue);
    }
  }
}
```

**Example (merge instead of overwrite)**
- If you already have `derivationEntry` for an identifier, update it by: `typeOfValue = join(existing.typeOfValue, incoming.typeOfValue)` and `sourcesIds = union(existing.sourcesIds, incoming.sourcesIds)`.

Following this standard prevents subtle analysis/optimization bugs caused by overwriting, incomplete propagation coverage, or structurally invalid rewrites.