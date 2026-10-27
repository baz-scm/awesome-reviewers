---
title: Cache Ordering And Reuse
description: 'When code relies on cached state for multi-pass/fixpoint logic, treat
  caching as both a correctness dependency and a performance concern.


  Apply these rules:'
repository: facebook/react#b14
label: Caching
language: TypeScript
comments_count: 2
repository_stars: 251893
---

When code relies on cached state for multi-pass/fixpoint logic, treat caching as both a correctness dependency and a performance concern.

Apply these rules:
1) **Maintain cache correctness via ordering**: Record all prerequisite derivations/phi results before walking instructions that read them from cached context. If you introduce snapshots (e.g., `takeSnapshot()`), ensure they occur after the cache has been populated with the data needed by the subsequent traversal.
2) **Reuse intermediates inside loops**: Don’t repeatedly construct identical helper structures (like `new Set(...)`) within `filter/map` chains or hot loops—compute once per iteration and reuse.
3) **Use lazy diagnostics only when justified**: For expensive error-only computations, lazy functions/closures are fine if they clearly avoid work on the common path. If the benefit is unclear, keep the code simpler (eager computation or a straightforward `Set`).

Example (reuse cached `Set` to avoid O(n^2)):
```ts
const rvaluesUnfiltered = Array.from(phi.operands.values());
// Compute once
const rvaluesSet = new Set(rvalues);

// BAD: repeatedly creating Set inside filter
// rvaluesUnfiltered.filter(v => new Set(rvalues).has(v))

const undefineds = rvaluesUnfiltered.filter(v => rvaluesSet.has(v));
```

Example (cache correctness/order for fixpoint traversal):
```ts
// Ensure phis are recorded before traversing instructions that depend on them.
for (const block of fn.body.blocks.values()) {
  recordPhiDerivations(block, context);
}

context.derivationCache.takeSnapshot();
// Now walk instructions that read derived values from cache/context
for (const block of fn.body.blocks.values()) {
  for (const inst of block.instructions) {
    // reads from context/derivation cache
  }
}
```