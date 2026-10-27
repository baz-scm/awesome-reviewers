---
title: Precise Contract, Minimal Context
description: 'When designing or updating API surfaces (including internal “function
  signature” models), keep two invariants:


  1) Be precise about the contract. Encode the exact parameter/effect/return semantics
  of the operation—especially distinctions like positional vs rest parameters and
  effect kinds.'
repository: facebook/react#b8
label: API
language: TypeScript
comments_count: 2
repository_stars: 251889
---

When designing or updating API surfaces (including internal “function signature” models), keep two invariants:

1) Be precise about the contract. Encode the exact parameter/effect/return semantics of the operation—especially distinctions like positional vs rest parameters and effect kinds.
2) Keep interfaces minimal. If the callee (or its owned context) already has access to the needed data, don’t thread redundant parameters through the call chain.

How to apply:
- Signature modeling: ensure the shape/effect metadata matches the real call form.
  - Example (signature precision): for `with(index, value)` model parameter effects explicitly, e.g. `positionalParams: [Effect.Read, Effect.Capture]`.
- Interface design: if the callee can read environment/context from the object it already owns, avoid passing `env`/context as extra arguments.

Practical checklist for API changes:
- Did we update the contract metadata (parameter kinds/effects/returns) to match the exact operation?
- Did we remove unnecessary parameters when existing context is already available to the callee?
- Are validations (or downstream behaviors) consistent with the contract semantics we encoded?