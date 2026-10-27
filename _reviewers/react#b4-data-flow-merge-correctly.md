---
title: Data-flow Merge Correctly
description: When implementing compiler/data-flow algorithms (derivation caches, CFG
  rewrites, effect/dependency validation), preserve correctness by (1) using scope-aware
  binding checks, (2) validating any IR/CFG structural assumptions before rewriting,
  and (3) merging derived facts instead of overwriting them.
repository: facebook/react#b4
label: Algorithms
language: TypeScript
comments_count: 6
repository_stars: 251885
---

When implementing compiler/data-flow algorithms (derivation caches, CFG rewrites, effect/dependency validation), preserve correctness by (1) using scope-aware binding checks, (2) validating any IR/CFG structural assumptions before rewriting, and (3) merging derived facts instead of overwriting them.

Practical rules:
- Scope-aware transforms: if rewriting/global-special-casing something like `Symbol`, check the actual binding (e.g., `binding.kind === 'Global'`) so shadowed locals/params aren’t rewritten.
- CFG/shape gating: before replacing an instruction/terminator based on a value, confirm the target CFG shape matches your algorithm’s model (e.g., branch blocks are the expected kind; fallthrough/goto targets won’t contain nested value blocks you didn’t handle).
- Cache merge semantics: when a derivation entry already exists, update it by joining/merging (type/value kind and sources) rather than replacing it.
- Prefer generic propagation helpers: mark all relevant lvalues by scanning operands for “derived-from-X” properties, instead of enumerating only a few instruction kinds.

Code sketch (derivation merge):
```ts
// BAD: overwrites existing derivation
cache.set(placeId, {typeOfValue: currentType, sourcesIds});

// GOOD: merge/join with existing
const prev = cache.get(placeId);
const mergedType = joinValue(prev?.typeOfValue ?? 'ignored', currentType);
const mergedSources = new Set([...(prev?.sourcesIds ?? []), ...sourcesIds]);
cache.set(placeId, {typeOfValue: mergedType, sourcesIds: mergedSources});
```

If you discover an assumption mismatch (scope shadowing, unexpected memoization/data-structure shape, or CFG shape differences), add a minimal failing fixture and update the algorithm so the model matches the observed IR.