---
title: Runtime Error-Tolerance
description: When the system’s behavior around exceptions is intentionally permissive
  (e.g., in effect handling), codify that policy and validate it with fixtures that
  fail for the right reasons.
repository: facebook/react#b3
label: Error Handling
language: Markdown
comments_count: 2
repository_stars: 251883
---

When the system’s behavior around exceptions is intentionally permissive (e.g., in effect handling), codify that policy and validate it with fixtures that fail for the right reasons.

Apply these rules:
1) **Explicitly specify “throw vs don’t throw”** for uncertain side effects (e.g., global function calls inside effects). If the contract is “don’t throw,” ensure the implementation and tests enforce that expectation (assert that execution completes without exceptions).
2) **Make test inputs runtime-real**, not type-only. If a fixture uses a declaration that exists only in the type system, compiled output may throw unrelated runtime errors (e.g., `ReferenceError`) and mask the behavior you actually want to test.

Example (avoid type-only stubs causing misleading runtime exceptions):
```ts
// Bad: type-only declaration leads to runtime failure like “id is not defined”
declare function id<T>(x: T): T;

// Good: real runtime function so the test validates the intended error behavior
function id<T>(x: T): T {
  return x;
}

export function test<T = string>(value = id<string>('hi')) {
  return value;
}
```

For effect/global-call scenarios, pair this with an assertion that the transformation/execution **does not throw** in the designated “no-error” path.