---
title: Precise Parameter Effects
description: When defining any function/method “contract” that includes semantic effects
  (e.g., read/write/capture/mutate/conditionally mutate), model each argument’s role
  precisely and positionally. Don’t lump distinct behaviors into a single generic/rest
  effect—use explicit positional effect annotations when argument semantics differ.
repository: facebook/react#b2
label: API
language: TypeScript
comments_count: 2
repository_stars: 251882
---

When defining any function/method “contract” that includes semantic effects (e.g., read/write/capture/mutate/conditionally mutate), model each argument’s role precisely and positionally. Don’t lump distinct behaviors into a single generic/rest effect—use explicit positional effect annotations when argument semantics differ.

Apply this by:
- Mapping each parameter to its actual semantic role (e.g., the value being inserted vs indexes used to find positions).
- Encoding those roles in the signature using positional effect lists when different arguments have different effects.
- Adding a brief comment when the effect is non-obvious (e.g., because a value flows into a lambda and may be mutated).

Example (effect modeling):
```ts
// fill(value, start, end)
addFunction(..., {
  // value is stored into the array
  positionalParams: [Effect.Capture],
  // start/end are only read
  restParam: Effect.Read,
  calleeEffect: Effect.Store,
});

// with(index, value)
addFunction(..., {
  positionalParams: [Effect.Read, Effect.Capture],
  restParam: null,
  calleeEffect: Effect.Store,
});
```