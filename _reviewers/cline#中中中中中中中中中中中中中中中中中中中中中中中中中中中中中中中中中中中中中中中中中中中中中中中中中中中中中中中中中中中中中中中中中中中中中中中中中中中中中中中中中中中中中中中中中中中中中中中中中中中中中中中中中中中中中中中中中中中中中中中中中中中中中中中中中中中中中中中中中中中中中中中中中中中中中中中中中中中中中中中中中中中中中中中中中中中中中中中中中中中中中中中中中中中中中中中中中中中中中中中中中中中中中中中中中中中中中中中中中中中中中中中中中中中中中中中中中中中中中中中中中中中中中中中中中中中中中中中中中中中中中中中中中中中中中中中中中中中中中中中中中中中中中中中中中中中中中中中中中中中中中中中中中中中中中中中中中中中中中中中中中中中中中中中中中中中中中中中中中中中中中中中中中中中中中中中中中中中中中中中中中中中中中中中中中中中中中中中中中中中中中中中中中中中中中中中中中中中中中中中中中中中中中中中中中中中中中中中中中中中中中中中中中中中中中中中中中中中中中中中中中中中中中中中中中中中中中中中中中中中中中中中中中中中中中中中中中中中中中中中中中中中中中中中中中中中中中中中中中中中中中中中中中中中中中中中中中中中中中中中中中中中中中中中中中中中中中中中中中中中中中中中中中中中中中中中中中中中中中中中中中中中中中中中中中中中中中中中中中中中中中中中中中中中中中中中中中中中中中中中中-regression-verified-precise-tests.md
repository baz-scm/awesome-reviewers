---
title: Regression-verified, precise tests
description: 'A test only earns its keep if it can actually fail for the bug it claims
  to guard against. Several reviews caught tests that passed by accident: a matcher
  that short-circuits on `undefined` instead of failing (discussion 3), fixtures that
  all shared an unrelated keyword so the field actually under test was never exercised
  alone (discussion 4), a bound so...'
repository: cline/cline#中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中
label: Testing
language: TypeScript
comments_count: 17
repository_stars: 70984
---

A test only earns its keep if it can actually fail for the bug it claims to guard against. Several reviews caught tests that passed by accident: a matcher that short-circuits on `undefined` instead of failing (discussion 3), fixtures that all shared an unrelated keyword so the field actually under test was never exercised alone (discussion 4), a bound so loose ("less than 1/10th of a naive estimate") that a wrong implementation could still pass (discussions 11, 12), or a plural-form check that stripped away the exact suffixes it should have required (discussion 23). When you add or change behavior:

1. **Assert the exact expected shape/value**, not a loose bound or a matcher that can silently no-op. Prefer `expect(x).toBe(exact)` or `toMatchObject({ a, b, c })` over `toBeLessThan(fudge)`, and make sure the assertion actually dereferences the value (`should(value)`, not `value?.should`).
2. **Prove the test would fail without the fix.** Revert the change, mutate the implementation, or point to the bug reproduction and confirm red-before/green-after (discussions 6, 16, 18, 21, 26). This is the cheapest way to catch a vacuous test before it ships.
3. **Exercise the real boundary when the bug lives there.** If a cast, adapter hand-off, or retry/backoff path only breaks against the real dependency, don't mock it away — drive the real SDK/adapter with a stubbed transport (fetch, socket) so the integration is actually covered (discussions 5, 21). Conversely, don't duplicate a third-party library's own behavior in your suite — scope tests to the code you own (discussion 25).
4. **Isolate test state.** Restore environment variables with `vi.stubEnv`/`vi.unstubAllEnvs` (or manual save/restore) rather than leaving them mutated (discussion 20, 17), and stub the specific method that produces unwanted side effects (e.g., a never-ending stream) instead of letting a background listener or timer outlive the test (discussion 15).

Example of turning a loose bound into a precise, regression-proof assertion:
```ts
// Weak: passes even if the implementation charges something close to proportional.
expect(tokens).toBeLessThan(naiveCharBasedEstimate / 10);

// Precise: pins the exact flat-rate behavior and is independent of payload size.
const perImage = estimate("A".repeat(500_000)) - estimate("A");
expect(perImage).toBe(0); // payload length must not move the estimate at all
```