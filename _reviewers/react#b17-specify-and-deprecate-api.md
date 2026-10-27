---
title: Specify And Deprecate API
description: 'Treat API surface and API semantics as contracts: changes must be communicated
  via deprecation when there’s any chance of external or downstream reliance, and
  the contract must precisely encode the real behavior (including side effects) rather
  than an approximation.'
repository: facebook/react#b17
label: API
language: TypeScript
comments_count: 2
repository_stars: 251891
---

Treat API surface and API semantics as contracts: changes must be communicated via deprecation when there’s any chance of external or downstream reliance, and the contract must precisely encode the real behavior (including side effects) rather than an approximation.

Apply:
- When removing/renaming an exposed option or field: prefer `deprecated` + documentation/changelog notice before removal; only classify as “non-breaking” after confirming no downstream consumers rely on it.
- When defining types/effects for a callable: make the contract match parameter-by-parameter behavior (e.g., reads vs writes), especially for subtle semantics.

Example (effect-accurate contract):
```ts
// For fill(value, start, end): value is written into the array (Capture),
// while start/end are read.
addFunction(BUILTIN_SHAPES, [], {
  positionalParams: [Effect.Capture],
  restParam: Effect.Read,
  returnType: { kind: 'Object', shapeId: BuiltInArrayId },
  calleeEffect: Effect.Store,
  returnValueKind: ValueKind.Mutable,
});
```

If you can’t express the exact semantics, don’t ship an approximated contract—either refine the model or document the limitation clearly.