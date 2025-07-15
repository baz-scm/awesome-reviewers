---
title: "Verify types in tests"
description: "Use explicit type assertions in TypeScript tests to verify that types behave as expected across various scenarios. Include assertions for inheritance relationships, property types, and different response status codes."
repository: "fastify/fastify"
label: "Testing"
language: "TypeScript"
comments_count: 2
repository_stars: 34000
---

Use explicit type assertions in TypeScript tests to verify that types behave as expected across various scenarios. Include assertions for inheritance relationships, property types, and different response status codes. This helps catch type-related regressions early and ensures the type system correctly models your application's behavior.

Example:
```ts
instance.register(childInstance => {
  // Verify inherited properties maintain correct types
  expectType<void>(childInstance.testPropSync)
  expectType<string>(childInstance.testValueSync)
  expectType<number>(childInstance.testFnSync())
})

// Verify response types with different status codes
expectType<(payload?: string) => typeof res>(res.code(200).send)
// Add assertions for other status codes
```