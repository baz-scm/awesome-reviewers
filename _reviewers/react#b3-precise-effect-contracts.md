---
title: Precise Effect Contracts
description: When adding or updating API-like contracts (e.g., function effect/side-effect
  signatures), make the contract match the real runtime semantics for each parameter
  role and position, and avoid unnecessary plumbing of context that the callee already
  has.
repository: facebook/react#b3
label: API
language: TypeScript
comments_count: 3
repository_stars: 251883
---

When adding or updating API-like contracts (e.g., function effect/side-effect signatures), make the contract match the real runtime semantics for each parameter role and position, and avoid unnecessary plumbing of context that the callee already has.

Apply this by:
- For each built-in function signature, determine which arguments are read vs stored/captured vs conditionally mutate, and encode that in `positionalParams` and `restParam` accordingly (don’t approximate with a single coarse effect).
- If the callee already has access to required context via its receiver (e.g., the HIR/value object), prefer using that instead of threading extra parameters through the API.
- When behavior is subtle (e.g., “first arg is stored, others are read”), document the mapping so the contract doesn’t drift.

Example (effect contract precision):
```ts
// fill(value, start, end): value is stored, start/end are read
addFunction(BUILTIN_SHAPES, [], {
  positionalParams: [Effect.Capture],
  restParam: Effect.Read,
  calleeEffect: Effect.Store,
  returnValueKind: ValueKind.Mutable,
});

// with(index, value): index is read, value is captured
addFunction(BUILTIN_SHAPES, [], {
  positionalParams: [Effect.Read, Effect.Capture],
  restParam: null,
  calleeEffect: Effect.Store,
});
```