---
title: Be Real in Error Tests
description: When validating error handling (especially “should not throw” scenarios),
  make sure (1) the runtime behavior under uncertainty is explicitly encoded in the
  test fixture expectations, and (2) the fixture inputs are real runtime values—not
  type-only declarations—so failures reflect actual execution.
repository: facebook/react#b12
label: Error Handling
language: Markdown
comments_count: 2
repository_stars: 251896
---

When validating error handling (especially “should not throw” scenarios), make sure (1) the runtime behavior under uncertainty is explicitly encoded in the test fixture expectations, and (2) the fixture inputs are real runtime values—not type-only declarations—so failures reflect actual execution.

Application checklist:
- If the behavior is “must not throw” due to uncertain global/side effects, document it in the fixture naming/expectations (e.g., “no-error”) and ensure the test covers that unknown global call.
- For runtime/eval-based tests, avoid TypeScript-only stubs (e.g., `declare function`) when the evaluator executes JavaScript/Node; provide an actual function implementation.

Example (runtime-safe fixture):
```ts
// Bad: type-only, may fail at runtime eval
// declare function id<T>(x: T): T;

// Good: concrete runtime function to exercise real error handling
function id<T>(x: T): T {
  return x;
}

export function test<T = string>(value = id<string>("hi")) {
  return value;
}
```

If a global function call occurs inside an effect and side effects are uncertain, ensure the implementation and the corresponding tests enforce the intended “no throw” behavior rather than failing due to assumptions about what the global might do.