---
title: Iterative dataflow algorithm correctness
description: 'When implementing iterative or fixpoint algorithms over graphs (e.g.
  dataflow analyses on CFGs), pay close attention to processing order, state accumulation,
  and complexity:'
repository: facebook/react#b19
label: Algorithms
language: TypeScript
comments_count: 3
repository_stars: 251893
---

When implementing iterative or fixpoint algorithms over graphs (e.g. dataflow analyses on CFGs), pay close attention to processing order, state accumulation, and complexity:

1. Respect data dependencies when ordering work within a pass. If a block's phis define values consumed by that block's instructions, process phis before instructions in the same iteration, not after. Processing out of order can leave the analysis cache missing values and silently produce incorrect results, e.g.:
```js
let x = thing1; // x@0
if (cond) {
  x = {}; // x@1
}
// x@2 = phi(x@0, x@1)
doSomething(x) // references x@2 - requires phi already recorded
```

2. When updating per-identifier/per-node state across multiple passes of a fixpoint computation, merge new information with the existing entry rather than overwriting it. Overwriting can discard previously-derived facts and break convergence or correctness:
```js
// Wrong: discards prior derivation info
context.derivationCache.set(id, {sources, typeOfValue});

// Right: join with any existing entry
const existing = context.derivationCache.get(id);
context.derivationCache.set(id, mergeDerivation(existing, {sources, typeOfValue}));
```

3. Watch for accidental quadratic behavior inside loops that run per-node or per-pass, such as allocating a new `Set`/array on every iteration to do a containment check. Hoist and cache such structures outside the hot loop, or restructure the check to avoid repeated O(n) work per element, which otherwise turns an O(n) pass into O(n^2):
```js
// Wrong: new Set allocated on every iteration, O(n^2) overall
for (const item of items) {
  const set = new Set(candidates);
  if (set.has(item)) { ... }
}

// Right: build the Set once outside the loop
const set = new Set(candidates);
for (const item of items) {
  if (set.has(item)) { ... }
}
```

Before merging a new iterative/graph algorithm, verify: inputs are available in the order they're needed, state updates join rather than clobber prior results, and no per-iteration work introduces unintended quadratic cost.</description>
