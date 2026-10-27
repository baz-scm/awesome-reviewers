---
title: Sound dataflow algorithms
description: 'When implementing iterative/fixed-point dataflow or graph algorithms
  (e.g. derivation tracking, escape analysis, value-kind inference), verify the following
  algorithmic properties rather than just the happy path:'
repository: facebook/react#b20
label: Algorithms
language: TypeScript
comments_count: 6
repository_stars: 251895
---

When implementing iterative/fixed-point dataflow or graph algorithms (e.g. derivation tracking, escape analysis, value-kind inference), verify the following algorithmic properties rather than just the happy path:

1. **Merge, don't overwrite.** When an instruction or node has multiple incoming values (phi operands, re-assigned lvalues, joined abstract values), combine them with an explicit join/merge function instead of letting the last write clobber prior state. For example, `mergeValueKinds()` must treat `ShallowMutable` like `Mutable` when joining with other kinds (`Mutable | x => Mutable`, `ShallowMutable | x => ShallowMutable`, but `ShallowMutable | Mutable => Mutable`), and derivation entries should be merged with the operand's existing entry rather than replaced.

2. **Collect all contributing values, not just the last one.** When an instruction produces multiple related outputs (e.g. all bindings in a `Destructure` pattern), make sure the algorithm aggregates dependencies/results across all of them instead of only keeping the final one:
```js
// Wrong: `dep` ends up only tracking the last destructured property
for (const storeTarget of eachInstructionValueLValue(value)) {
  dep = { root: { kind: 'NamedLocal', value: storeTarget }, path: [] };
}
```

3. **Guard recursive/graph traversals against cycles.** Any recursive walk over a potentially cyclic structure (e.g. chasing `LoadLocal` chains to find a root `setState`) must track visited nodes and bail out safely instead of risking infinite recursion.

4. **Respect data-dependency ordering in iterative passes.** When a pass depends on values defined earlier in the same iteration (e.g. phis defining values used by subsequent instructions in a block), process them in the correct order on every pass of the fixpoint loop — don't reorder steps arbitrarily when debugging, as doing so can silently drop needed state.

5. **Watch for accidental quadratic blowup.** Avoid re-deriving or re-allocating data structures (e.g. constructing a new `Set` per iteration) inside loops; hoist/cache such structures, and prefer lazy computation of expensive diagnostics only when an error path is actually hit.

Before merging a new analysis/graph algorithm, add test cases that exercise joins across different abstract states and cyclic/branching control flow to confirm the merge and traversal logic behave correctly.