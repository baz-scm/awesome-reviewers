---
title: Test real behavior, strictly
description: 'A test only protects a behavior if it actually runs that behavior''s
  real code and fails when that code regresses. Several bugs slipped past tests that
  looked thorough but weren''t: an assertion chain that short-circuits on `undefined`
  instead of failing (`value?.should.deepEqual(...)`), a test asserting against an
  inline copy of the mapping table instead of...'
repository: cline/cline#1
label: Testing
language: TypeScript
comments_count: 14
repository_stars: 71024
---

A test only protects a behavior if it actually runs that behavior's real code and fails when that code regresses. Several bugs slipped past tests that looked thorough but weren't: an assertion chain that short-circuits on `undefined` instead of failing (`value?.should.deepEqual(...)`), a test asserting against an inline copy of the mapping table instead of calling the real `getWindowsConsoleEncoding()`, a plural-catalog test that stripped the exact suffixes it was supposed to verify, and provider "wire" tests that mocked the SDK adapter so deeply that the real request-building code never ran.

When writing or reviewing a test:
- Prefer driving the real function/module under test (and, for integration points like HTTP providers, the real third-party SDK) over re-implementing its logic inline or mocking away the code path you actually need to verify. If you must mock, mock at the true boundary (e.g., `fetch`), not the unit under test.
- Make assertions that cannot pass silently: use `should(value).deepEqual(...)` instead of `value?.should...`, assert on a precise expected value/shape instead of a loose range, and verify a negative test case fails without the fix (mutate the implementation locally to confirm).
- Cover the edge cases that caused the bug or that the implementation explicitly handles — boundary lengths, disconnected clients, literal filenames with glob characters, gitlinks/symlinks, env-var precedence, missing required fields — not just the happy path.
- Where an invariant should hold across many inputs (e.g., "a skip hides only its row"), consider property-based/fuzz testing in addition to example-based tests, since it can catch cases a handful of examples miss.

Example of tightening a weak test:
```ts
// Weak: passes even if annotations are dropped, because `?.` short-circuits.
server.tools?.[0].annotations?.should.deepEqual({ ... })

// Strong: fails loudly if annotations is undefined.
should(server.tools?.[0].annotations).deepEqual({ ... })
```