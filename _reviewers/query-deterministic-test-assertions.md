---
title: Deterministic Test Assertions
description: 'For tests, prefer deterministic, intention-revealing assertions and
  keep runtime tests and type-only tests strictly separated.


  Apply:

  1) Use the right matcher for the claim'
repository: tanstack/query
label: Testing
language: TSX
comments_count: 12
repository_stars: 49380
---

For tests, prefer deterministic, intention-revealing assertions and keep runtime tests and type-only tests strictly separated.

Apply:
1) Use the right matcher for the claim
- Identity: use `toBe` instead of deep equality when referential identity matters.
- Async rejections: prefer matcher-based assertions over try/catch.

2) Make timer-based tests fast and stable
- If you must use timers, prefer fake timers and advance/run them deterministically.
- Keep real timer durations extremely short.

3) Don’t mix runtime and type-only tests
- Put compile-time checks into `*.test-d.tsx` and use `expectTypeOf(...).toEqualTypeOf(...)`.
- In `*.test-d.tsx`, don’t rely on runtime behavior inside `it` blocks.

4) Ensure the test can prove which code path executed
- When a hook can call different `queryFn`s (e.g., prefetch vs render), use distinct spies and assert call counts. Clear mocks after setup calls.

Example (async rejection + timers + type-only):
```ts
// runtime test
await expect(promise).rejects.toBe(testError)

// timer test (prefer fake timers)
vi.useFakeTimers()
vi.runAllTimersAsync()
expect(spy).toHaveBeenCalledTimes(0)

// type-only test in *.test-d.tsx
expectTypeOf(result4[0]).toEqualTypeOf<UseQueryResult<string, Error>>()
```

This reduces brittle/flaky tests, improves signal-to-noise, and guarantees type coverage lives where it’s actually executed by the tooling.