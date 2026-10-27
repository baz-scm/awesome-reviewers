---
title: Invariant-Driven Transforms
description: 'When implementing optimization or transformation passes (AST/HIR/CFG),
  treat semantic preconditions as first-class invariants. Concretely:


  1) State the invariant your pass assumes (scope/binding identity, CFG shape, value-block
  rules, dependency roots, fixed-point convergence).'
repository: facebook/react#b13
label: Algorithms
language: TypeScript
comments_count: 6
repository_stars: 251893
---

When implementing optimization or transformation passes (AST/HIR/CFG), treat semantic preconditions as first-class invariants. Concretely:

1) State the invariant your pass assumes (scope/binding identity, CFG shape, value-block rules, dependency roots, fixed-point convergence).
2) Enforce it with targeted structural checks; if it doesn’t match, skip or fall back. (Example: ternary constant propagation should verify the target control-flow shape before rewriting.)
3) Add invariants that are stronger than local checks when possible, and validate across both backends.
4) Pair the rewrite with regression fixtures that exercise the exact tricky edges (shadowing, outlining context boundaries, destructuring semantics, shifted/missing offset handling).

Example (global invariant check + regression coverage idea):
```ts
// After transforming output AST, verify location/range mapping globally.
for (const node of outputAst.nodes()) {
  if (typeof node.start === 'number' && typeof node.end === 'number' && node.loc?.index != null) {
    assert(node.start === node.loc.start.index);
    assert(node.end === node.loc.end.index);
    assert(node.start <= node.end);
  }
}
// Then add fixtures that cover shifted and partial offsets across both backends.
```

This keeps algorithmic rewrites correct as the codebase evolves, especially when passes depend on subtle semantic modeling (scoping, binding kinds, data-flow sources, and control-flow shape).