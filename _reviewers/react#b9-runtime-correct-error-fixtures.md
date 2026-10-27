---
title: Runtime-Correct Error Fixtures
description: When adding error-handling test fixtures, make the “throw vs no-throw”
  contract explicit and ensure the fixture is actually executable at runtime. Otherwise,
  you risk either (a) misleading expectations (e.g., a `-no-error` fixture name doesn’t
  match the implemented behavior) or (b) spurious exceptions that obscure the real
  error-handling behavior.
repository: facebook/react#b9
label: Error Handling
language: Markdown
comments_count: 2
repository_stars: 251891
---

When adding error-handling test fixtures, make the “throw vs no-throw” contract explicit and ensure the fixture is actually executable at runtime. Otherwise, you risk either (a) misleading expectations (e.g., a `-no-error` fixture name doesn’t match the implemented behavior) or (b) spurious exceptions that obscure the real error-handling behavior.

Apply:
- Align fixture names/variants with the intended error policy. If the rule is “don’t throw for global function calls in effects because we can’t know whether they trigger state updates,” the fixture naming and comments should state that rationale.
- Ensure eval/test inputs use real runtime bindings, not type-only declarations. If an eval output shows “X is not defined,” fix the fixture setup rather than accepting the failure.

Example pattern (runtime binding instead of type-only):
```ts
// Bad: type-only, can lead to runtime “not defined”
declare function id<T>(x: T): T;

// Good: executable function so error-handling is testable
function id<T>(x: T): T {
  return x;
}

export function test<T = string>(value = id<string>("hi")) {
  return value;
}
```

Checklist:
- Does the fixture name communicate the exact expected error behavior?
- If the fixture is evaluated, are all symbols defined at runtime?
- Do comments explain why an exception is intentionally suppressed (e.g., uncertain side effects)?