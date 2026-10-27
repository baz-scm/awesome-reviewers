---
title: Fixpoint dataflow correctness
description: When implementing iterative/fixpoint algorithms over a CFG (e.g., dataflow
  analyses that process phis and instructions until no changes occur), pay special
  attention to processing order and merge semantics, and avoid accidental quadratic
  blowups.
repository: facebook/react#b18
label: Algorithms
language: TypeScript
comments_count: 4
repository_stars: 251889
---

When implementing iterative/fixpoint algorithms over a CFG (e.g., dataflow analyses that process phis and instructions until no changes occur), pay special attention to processing order and merge semantics, and avoid accidental quadratic blowups.

1. Processing order: process each block's phis before its instructions, since phis define values (e.g., `x@2 = phi(x@0, x@1)`) that later instructions in the same block depend on. Reordering this can silently leave the analysis state missing values that downstream instructions need.

```js
let x = thing1; // x@0
if (cond) {
  x = {}; // x@1
}
// x@2 = phi(x@0, x@1)  <-- must be recorded before visiting instructions below
doSomething(x); // references x@2
```

2. Merge semantics: when an operand or identifier already has an entry in a cache/lattice (e.g., a derivation-type cache or an abstract value-kind lattice), new information must be *joined* with the existing entry, not overwrite it. Define an explicit join/merge function with documented precedence rules (e.g., `Mutable | ShallowMutable => Mutable`, but `ShallowMutable | ShallowMutable => ShallowMutable`) and use it consistently so the fixpoint converges to the correct, monotonic result. Add targeted tests for cases where values merge from different branches to catch incorrect joins early.

3. Complexity: when building graphs or caches inside loops (e.g., over instructions/phis), avoid re-creating data structures (like `new Set(...)`) on every iteration purely to do membership checks — this turns a linear pass into O(n²). Hoist or cache such structures outside the loop, and only pay for expensive diagnostic computations (e.g., building detailed error info) lazily, when an error actually occurs, rather than eagerly on every iteration.

Applying these three checks — correct visitation order, correct join operations, and avoiding redundant per-iteration allocations — prevents subtle correctness bugs and performance regressions in dataflow-style algorithms.</description>
</invoke>
