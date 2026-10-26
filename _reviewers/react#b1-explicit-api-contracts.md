---
title: Explicit API Contracts
description: 'When changing or defining an API (including compiler options and internal
  type/effect contracts), make the contract explicit, cohesive, and stable.


  - Prefer deprecation over removal for options/config flags. Even if an option isn’t
  documented, assess whether removal is a breaking change and handle it via deprecation
  when in doubt.'
repository: facebook/react#b1
label: API
language: TypeScript
comments_count: 3
repository_stars: 251878
---

When changing or defining an API (including compiler options and internal type/effect contracts), make the contract explicit, cohesive, and stable.

- Prefer deprecation over removal for options/config flags. Even if an option isn’t documented, assess whether removal is a breaking change and handle it via deprecation when in doubt.
- Keep function signatures cohesive: don’t thread context objects (e.g., environment) through parameters if the callee/object already has access to it.
- Make semantic contracts precise: for typed/effectful APIs, annotate which arguments are read vs captured/stored (and which are immutable vs mutable) so downstream logic is correct.

Example (precise semantic contract):
```ts
// fill(value, start, end): value is stored; start/end are read
addFunction(BUILTIN_SHAPES, [], {
  positionalParams: [Effect.Capture],
  restParam: Effect.Read,
  returnType: {kind: 'Object', shapeId: BuiltInArrayId},
  calleeEffect: Effect.Store,
  returnValueKind: ValueKind.Mutable,
});
```

Example (interface cohesion):
```ts
// If `hir` already provides access to its environment, prefer:
validateExhaustiveDependencies(hir).unwrap();
// over:
validateExhaustiveDependencies(hir, env).unwrap();
```

Example (API stability):
- If considering removing a configuration option, first deprecate it (e.g., warn) and only remove after a full deprecation cycle and impact assessment.