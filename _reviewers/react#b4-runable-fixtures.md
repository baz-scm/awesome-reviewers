---
title: Runable Fixtures
description: 'When you add or edit a test fixture, ensure two things: (1) the fixture
  remains evaluatable at runtime (all referenced symbols exist), and (2) any test
  configuration/flags (e.g., output mode) don’t accidentally bypass the validation
  you’re trying to cover.'
repository: facebook/react#b4
label: Testing
language: Markdown
comments_count: 3
repository_stars: 251885
---

When you add or edit a test fixture, ensure two things: (1) the fixture remains evaluatable at runtime (all referenced symbols exist), and (2) any test configuration/flags (e.g., output mode) don’t accidentally bypass the validation you’re trying to cover.

Practical rules:
- If a fixture exports `FIXTURE_ENTRYPOINT`, assume the test runner will execute/evaluate the fixture code. Provide any required mocks/components it references.
- Don’t rely on type-only declarations for runtime values. If the fixture evaluation uses `id()` or renders a component, define real runtime functions/components.
- Only add/adjust special test directives (like output modes) when needed to reproduce or assert the intended failure; otherwise keep defaults so the test still checks the validation.

Example (fixing missing runtime symbols):
```js
// Bad: type-only declaration -> runtime error during eval
// declare function id<T>(x: T): T;

// Good: real runtime function
function id(x) { return x; }

export function test(value = id('hi')) {
  return value;
}

export const FIXTURE_ENTRYPOINT = {
  fn: test,
  params: [],
  isComponent: false,
};
```