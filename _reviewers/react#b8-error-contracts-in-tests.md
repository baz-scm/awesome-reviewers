---
title: Error Contracts In Tests
description: 'When defining or testing failure behavior, make the error-handling contract
  explicit and ensure fixtures exercise real runtime semantics.


  - If a scenario is intended to “not throw” (e.g., an effect containing a global
  function call), encode that expectation in the test/fixture and document the rationale
  (often you can’t know whether the global call will...'
repository: facebook/react#b8
label: Error Handling
language: Markdown
comments_count: 2
repository_stars: 251889
---

When defining or testing failure behavior, make the error-handling contract explicit and ensure fixtures exercise real runtime semantics.

- If a scenario is intended to “not throw” (e.g., an effect containing a global function call), encode that expectation in the test/fixture and document the rationale (often you can’t know whether the global call will trigger state updates).
- Avoid type-only placeholders in runtime-evaluated tests. If the compiled output will reference an identifier, define it as a real runtime function/value so exceptions reflect actual implementation/runtime behavior—not missing mocks.

Example (runtime-real fixture):
```ts
// Bad: type-only, will fail at runtime if used
// declare function id<T>(x: T): T;

// Good: runtime implementation so error output is meaningful
function id<T>(x: T): T {
  return x;
}

export function test<T = string>(value = id<string>('hi')) {
  return value;
}
```

Example (explicit no-throw intent for uncertain effects):
```js
// Pseudocode pattern for a “no-error” expectation:
try {
  // global call inside an effect should not surface exceptions
  globalThis.someGlobalFn();
} catch (e) {
  // suppress/convert only if the contract requires non-throw behavior
  // (and ensure a fixture asserts “no error”)
}
```

Use this to prevent (1) accidental exceptions caused by unrealistic test setup and (2) unclear/implicit “throw vs no-throw” behavior in failure scenarios.