---
title: Fail Loudly Invariants
description: Use `CompilerError.invariant` (or the project’s assertion mechanism)
  for internal assumptions that must never be violated, and ensure those failures
  are actionable (with `loc` where possible). Don’t rely on eslint to surface invariants—if
  an invariant can trip but isn’t reliably reported, the compiler may fail silently
  for some users.
repository: facebook/react#b12
label: Error Handling
language: TypeScript
comments_count: 4
repository_stars: 251896
---

Use `CompilerError.invariant` (or the project’s assertion mechanism) for internal assumptions that must never be violated, and ensure those failures are actionable (with `loc` where possible). Don’t rely on eslint to surface invariants—if an invariant can trip but isn’t reliably reported, the compiler may fail silently for some users.

Apply this when:
- Adding/maintaining HIR “shape” or metadata registries: missing definitions should trigger an invariant with a clear location/diagnostic rather than causing downstream resolution errors.
- Performing codegen/IR rewrites: if an invariant previously prevented an unsafe rewrite (e.g., method-call property transformation that can change receiver semantics), preserve an equivalent safety check or add targeted tests for the unsafe signature patterns.
- Building validation/diagnostic suggestions: propagate source `loc` through transformed/aggregated dependency representations so fixes can point back to the user’s manual deps array.

Example pattern:
```ts
// Prefer asserting internal invariants with actionable diagnostics.
CompilerError.invariant(isNamedIdentifier(sourceMetadata.place), {
  reason: 'Compiler internal error: derivation entries must reference named variables',
  loc: derivedVar.loc ?? null,
  description: null,
  suggestions: null,
});

// When transforming structures for diagnostics, preserve loc for later suggestion building.
type Aggregate = { kind: 'Aggregate'; dependencies: Set<InferredDependency>; loc: SourceLocation };
```

Outcome: compilation failures become deterministic, surfaced, and diagnosable—reducing both silent breakages and hard-to-debug crashes during validation/codegen.