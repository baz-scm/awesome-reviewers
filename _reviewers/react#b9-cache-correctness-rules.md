---
title: Cache correctness rules
description: When using a derivation/instruction cache, ensure cache entries are both
  (1) comprehensive and (2) populated in the correct phase before any consumer reads.
repository: facebook/react#b9
label: Caching
language: TypeScript
comments_count: 2
repository_stars: 251891
---

When using a derivation/instruction cache, ensure cache entries are both (1) comprehensive and (2) populated in the correct phase before any consumer reads.

Apply these rules:
1) Don’t narrow cache inputs without strong justification. If a predicate like `isNamedIdentifier` can exclude values that later computations depend on, update the cache to record those broader source cases (and add a fixture/regression test for the previously-missed scenario).
2) Update cache state before dependent analysis. For control-flow/SSA-like flows, record Phi derivations (and any other upstream cached facts) before walking blocks/instructions that read those cached types/values. If you introduce snapshots or refactors for loop/debugging, verify you didn’t change the required ordering.

Example pattern (ordering):
```js
let isFirstPass = true;
do {
  // If you snapshot for iterative refinement, still ensure upstream facts are recorded first.
  context.derivationCache.takeSnapshot();

  // Record phi-derived values for blocks so later instruction traversal can resolve types.
  for (const block of fn.body.blocks.values()) {
    recordPhiDerivations(block, context);
  }

  // Now it is safe to walk instructions that may consume phi results.
  // walkInstructions(...)

} while (/* cache changes */);
```

These two practices prevent stale or incomplete cache state that leads to missing derivations and incorrect downstream validations.