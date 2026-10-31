---
title: Tests must prove the behavior
description: 'A test is only as good as its ability to fail when the behavior it claims
  to check is wrong. Several reviews caught tests that looked thorough but could never
  catch the bug they were meant to guard against:'
repository: cline/cline?foo=bar
label: Testing
language: TypeScript
comments_count: 15
repository_stars: 71082
---

A test is only as good as its ability to fail when the behavior it claims to check is wrong. Several reviews caught tests that looked thorough but could never catch the bug they were meant to guard against:

- Assertions that short-circuit on `undefined`/`null` instead of failing (`value?.should.deepEqual(...)` vs. `should(value).deepEqual(...)`).
- Tests that assert against a hand-duplicated literal instead of calling the real function under test, so a change to the real implementation goes unnoticed.
- Fixtures where every case shares a confound (e.g. every "overloaded" fixture also contains the word "overloaded" in its message), so the specific field/code path being validated is never isolated.
- Fixtures that silently pass even when the fix is absent (e.g. a test double that stays alive when an env var is unset, or a case that never asserts the thing it implies, like confirming an id is actually excluded from a list rather than just not asserting on it).
- Mocking so much of the system that the real integration point (adapter wiring, process boundary, cast between library types) is never exercised.
- Async/lifecycle races baked into the test itself (asserting before a promise has actually settled, or leaking a pending call/timer past the test's teardown).

Before merging a new or changed test, verify it actually fails against the old/buggy code and passes only with the fix — mutate the implementation back and confirm the test catches it. Prefer driving the real function, the real adapter, or the real process over a hand-written duplicate or an over-mocked stand-in whenever the interaction itself is what you're testing. When a set of fixtures should each isolate one variable, make sure no other field in the fixture could also explain the result. Clean up shared/global state (env vars via `vi.stubEnv`/`unstubAllEnvs`, timers, pending async handles) so one test's fixture can't leak into another's.

Example of a weak vs. strong assertion:
```ts
// Weak: short-circuits to a pass when annotations is undefined.
server.tools?.[0].annotations?.should.deepEqual({ ... })

// Strong: fails loudly if annotations was dropped.
should(server.tools?.[0].annotations).deepEqual({ ... })
```