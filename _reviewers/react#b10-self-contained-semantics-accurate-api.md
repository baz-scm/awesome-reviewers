---
title: Self-contained, Semantics-Accurate API
description: When exposing API surfaces (configs, typed function models, schemas),
  ensure (1) the exported shape is self-contained (no placeholder objects that are
  later reassigned/mutated) and (2) the type-level contract is semantically accurate
  (reflect per-argument/behavior details rather than coarse approximations).
repository: facebook/react#b10
label: API
language: TypeScript
comments_count: 2
repository_stars: 251894
---

When exposing API surfaces (configs, typed function models, schemas), ensure (1) the exported shape is self-contained (no placeholder objects that are later reassigned/mutated) and (2) the type-level contract is semantically accurate (reflect per-argument/behavior details rather than coarse approximations).

Apply this as two practical rules:

1) Prefer self-contained API definitions
- Avoid patterns that export an object typed as a structure, then fill/replace it later.
- Prefer lazy/self-contained accessors for fields that depend on internal values.

Example (getter-based config shape):
```ts
const plugin = { /* ... */ };

export const configs = {
  recommended: {
    plugins: {
      get 'react-hooks'(): ESLint.Plugin {
        return plugin;
      },
    },
    rules: recommendedRuleConfigs,
  },
};

// And keep exported types decoupled from internal types:
// use `satisfies`/internal checks rather than baking `ESLint.Plugin` into exported type signatures.
```

2) Model runtime behavior precisely in the type contract
- If an API has argument-specific side effects/reads (or other behavioral nuances), encode them explicitly.
- Don’t rely on generic “reads/writes” labels when the runtime behavior differs per parameter.

Example (argument-by-argument effect precision):
```ts
// fill(value, start, end): value is written into the array; start/end are read.
addFunction(builtin, [], {
  positionalParams: [Effect.Capture],
  restParam: Effect.Read,
  returnType: { kind: 'Object', shapeId: BuiltInArrayId },
  calleeEffect: Effect.Store,
  returnValueKind: ValueKind.Mutable,
});
```

Outcome: exported APIs become easier to reason about (no placeholder mutation) and safer to consume (types match real semantics).