---
title: Fail Loudly With Invariants
description: 'When compiler internals rely on invariants or lookup completeness, treat
  violations as first-class errors: enforce them explicitly (with context) rather
  than letting downstream code throw an unreported invariant or silently skip.'
repository: facebook/react#b17
label: Error Handling
language: TypeScript
comments_count: 4
repository_stars: 251891
---

When compiler internals rely on invariants or lookup completeness, treat violations as first-class errors: enforce them explicitly (with context) rather than letting downstream code throw an unreported invariant or silently skip.

Apply these rules:
1) Assert internal assumptions at the boundary
- If a value must be a named identifier, add an explicit invariant where you first observe the value.

```ts
if (!isNamedIdentifier(sourceMetadata.place)) {
  CompilerError.invariant(isNamedIdentifier(sourceMetadata.place), {
    reason: "Compiler internal error: expected derivation entries to always reference named variables",
  });
}
```

2) Ensure declared ids have definitions
- If you register a built-in id/shape, also register its shape entry; otherwise property resolution can break in ways that are hard to diagnose.

```ts
addObject(BUILTIN_SHAPES, ReanimatedSharedValueId, []);
```

3) Carry source locations for actionable diagnostics/recovery
- For any validation input you may later use to build an automated fix, store `loc: SourceLocation` alongside the data so the compiler can generate precise suggestions instead of generic failures.

4) Only remove defensive logic after verifying the invariant
- If you’ve proven that an upstream function only supplies known ids, you may simplify—but encode the proof as an explicit `CompilerError.invariant` (or keep assertions) so future changes don’t reintroduce silent failures.