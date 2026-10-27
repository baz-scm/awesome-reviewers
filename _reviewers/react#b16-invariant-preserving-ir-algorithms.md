---
title: Invariant-Preserving IR Algorithms
description: 'When implementing compiler IR rewrites or dataflow/optimization passes,
  follow these algorithmic rules to keep transformations correct and conservative:'
repository: facebook/react#b16
label: Algorithms
language: TypeScript
comments_count: 4
repository_stars: 251891
---

When implementing compiler IR rewrites or dataflow/optimization passes, follow these algorithmic rules to keep transformations correct and conservative:

1) Preserve target invariants (structure + shape)
- Before/after any rewrite, ensure the emitted IR still satisfies the invariants of the target representation (e.g., what’s allowed inside a value block/`SequenceExpression`, or how CFG blocks are allowed to change).
- If the algorithm assumes a particular CFG/value-block shape, add explicit guards (or convert nested structures too), and back it with fixtures.

2) Be binding-identity aware (shadowing/conservatism)
- Never treat a name as “the global” unless you’ve verified the binding kind/scope information.
- If your pass rewrites `LoadGlobal`/symbol accesses, gate it on binding metadata that proves it’s truly global/unshadowed.

3) Use merge semantics for derived facts
- In dataflow-style logic (e.g., derivation caches, constant propagation), treat the derived information as facts in a lattice and merge with any existing facts.
- Avoid “set/overwrite” of derivation entries when multiple instructions/operands contribute to the same lvalue; overwrite tends to lose information and cause nondeterministic or order-dependent behavior.

Example (merge vs overwrite in a derivation cache)
```ts
// Wrong: overwrites prior facts
cache.set(lvalueId, { kind: computedKind, sources: computedSources });

// Right: merge computed facts with existing
const prev = cache.get(lvalueId);
const nextKind = mergeKinds(prev?.kind ?? 'ignored', computedKind);
const nextSources = union(prev?.sources ?? new Set(), computedSources);
cache.set(lvalueId, { kind: nextKind, sources: nextSources });
```

Example (shape guard for constant propagation)
- If you convert a ternary into a `goto`/break target, verify the target blocks don’t contain nested value-block constructs that also violate invariants; otherwise extend the conversion or add a stronger “safe-to-transform” check.

Finally: for each transformation, add at least one end-to-end fixture that targets the assumed shape/scope corner case (e.g., outlining-generated sequence expressions, shadowed `Symbol`, nested value-block control-flow, multi-source derivation merging).