---
title: Precise API Effect Contracts
description: 'When defining callable built-ins or validation entrypoints, make the
  “contract” explicit and exact:


  1) Match effects to argument semantics

  - Declare per-argument (positional vs rest) effect kinds to reflect what the runtime
  actually does (e.g., what is read vs captured/stored).'
repository: facebook/react#b6
label: API
language: TypeScript
comments_count: 3
repository_stars: 251888
---

When defining callable built-ins or validation entrypoints, make the “contract” explicit and exact:

1) Match effects to argument semantics
- Declare per-argument (positional vs rest) effect kinds to reflect what the runtime actually does (e.g., what is read vs captured/stored).
- If items flow through a callback and may be mutated there, use the appropriate conditional/aliasing and mutability constraints.

Example (more precise `fill`) 
```ts
addFunction(BUILTIN_SHAPES, [], {
  positionalParams: [Effect.Capture],
  restParam: Effect.Read,
  returnType: {kind: 'Object', shapeId: BuiltInArrayId},
  calleeEffect: Effect.Store,
  returnValueKind: ValueKind.Mutable,
});
```

2) Keep interfaces minimal when context is already available
- If an object (e.g., HIR) already has access to required context (e.g., environment), don’t pass that context through additional parameters just to make it available.

Practical checklist
- For each parameter position, ask: “Is this argument only read? Captured/stored? Does it become mutated via lambda flow?”
- Ensure any callback-related mutation is represented with the correct effect kind and constraints.
- Avoid redundant API parameters when the callee can access the needed context directly.