---
title: Fail Fast With Actionable Errors
description: 'When the compiler relies on internal registries or invariants, handle
  errors in a way that is both immediate and useful:


  - Validate completeness of referenced IDs at registration time (no “id exists but
  definition missing”). If an ID/shape is referenced, ensure its definition is added
  together with the registration, or throw a compiler error early.'
repository: facebook/react#b16
label: Error Handling
language: TypeScript
comments_count: 4
repository_stars: 251891
---

When the compiler relies on internal registries or invariants, handle errors in a way that is both immediate and useful:

- Validate completeness of referenced IDs at registration time (no “id exists but definition missing”). If an ID/shape is referenced, ensure its definition is added together with the registration, or throw a compiler error early.
- Replace ambiguous “continue / undefined handling” for compiler-contract assumptions with an explicit `CompilerError.invariant(...)` message. This prevents silent failures and turns internal inconsistencies into deterministic diagnostics.
- Preserve `loc: SourceLocation` (or equivalent) for any construct that could later produce a targeted “suggestion”/auto-fix. Diagnostics should be able to point to—and reconstruct—user-relevant code spans.

Example pattern:

```ts
// 1) Ensure referenced definitions exist (fail fast)
addObject(BUILTIN_SHAPES, ReanimatedSharedValueId, []);

// 2) Assert internal contracts (no silent continuation)
CompilerError.invariant(isNamedIdentifier(sourceMetadata.place), {
  reason: 'Compiler internal error: expected derivation entries to reference named variables',
});

// 3) Store loc for later suggestions/fixes
type TemporaryAggregate = {
  kind: 'Aggregate';
  dependencies: Set<InferredDependency>;
  loc: SourceLocation; // enables later suggestion targeting
};
```

Outcome: missing registries don’t slip into runtime/invariant explosions, internal state violations are reported deterministically, and diagnostics can generate actionable fixes instead of opaque failures.