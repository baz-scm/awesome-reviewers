---
title: Precise API Contracts
description: When designing exported APIs (including configuration surfaces and behavior/semantic
  annotations), make the contract self-contained and exactly reflect behavior.
repository: facebook/react#b11
label: API
language: TypeScript
comments_count: 3
repository_stars: 251894
---

When designing exported APIs (including configuration surfaces and behavior/semantic annotations), make the contract self-contained and exactly reflect behavior.

Apply these rules:
- Avoid “create placeholder object, then reassign/patch later” for public exports. Prefer deterministic, self-contained structures (e.g., getter-backed properties) so the API surface is correct at definition time.
- Keep exported types minimal. If internal types are needed only for validation, use `satisfies` rather than exposing internal implementation types.
- Precisely encode behavioral semantics in the API contract. If a parameter is captured/stored/mutates state, annotate it accordingly; don’t lump “mostly read” inputs into the same bucket.

Example (self-contained export + minimal typing):
```ts
const plugin = { /* meta + rules */ };

export const configs = {
  recommended: {
    plugins: {
      get 'react-hooks'() {
        return plugin; // deterministic, self-contained
      },
    },
    rules: recommendedRuleConfigs,
  },
} satisfies Record<string, { plugins: unknown; rules: Record<string, unknown> }>;
```

Example (precise parameter effects):
```ts
addFunction(BUILTIN_SHAPES, [], {
  positionalParams: [Effect.Capture], // `value` is stored
  restParam: Effect.Read,             // `start/end` are read-only
  returnType: { kind: 'Object', shapeId: BuiltInArrayId },
  calleeEffect: Effect.Store,
  returnValueKind: ValueKind.Mutable,
});
```

This prevents subtle contract drift where consumers (or downstream analysis) incorrectly assume read-only behavior or an unstable export shape.