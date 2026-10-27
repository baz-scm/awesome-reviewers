---
title: Actionable Error Context
description: All user-facing error/failure scenarios must be both (a) prevented or
  detected deterministically and (b) equipped with enough source context to produce
  clear, fixable diagnostics.
repository: facebook/react#b11
label: Error Handling
language: TypeScript
comments_count: 2
repository_stars: 251894
---

All user-facing error/failure scenarios must be both (a) prevented or detected deterministically and (b) equipped with enough source context to produce clear, fixable diagnostics.

- Validate cross-references early: when you register/introduce an identifier (e.g., a shape id, key, enum member), ensure the corresponding definition exists. Don’t rely on “invariant”-style crashes that may not be reported by lint tooling; instead, either add the missing definition or raise a clear, compiler-level error.
- Preserve source context for automated suggestions: when collecting data needed to build an error message or an automated fix, store source location (e.g., `loc: SourceLocation`) so the compiler can point to the exact range and generate precise `suggestion` text.

Example pattern (definition completeness):
```ts
// Ensure registry entries always have definitions
addObject(BUILTIN_SHAPES, BuiltInRefValueId, [['*', { kind: 'Object', shapeId: BuiltInRefValueId }]]);
addObject(BUILTIN_SHAPES, ReanimatedSharedValueId, []); // missing definition -> invariant/silent failure risk
```

Example pattern (context for suggestions):
```ts
type Temporary =
  | { kind: 'Function'; dependencies: Set<Temporary> }
  | { kind: 'Aggregate'; dependencies: Set<InferredDependency>; loc: SourceLocation };

// Later: use `loc` to build an automated fix/suggestion at the correct location.
```