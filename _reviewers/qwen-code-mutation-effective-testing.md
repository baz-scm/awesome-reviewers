---
title: Mutation-Effective Testing
description: 'Ensure your tests are *mutation-effective*: they must fail when the
  implementation changes in ways that break intended behavior. Avoid vacuous assertions,
  and don’t confuse “a test exists” with “the test would catch the real bug.”'
repository: QwenLM/qwen-code
label: Testing
language: TypeScript
comments_count: 7
repository_stars: 26407
---

Ensure your tests are *mutation-effective*: they must fail when the implementation changes in ways that break intended behavior. Avoid vacuous assertions, and don’t confuse “a test exists” with “the test would catch the real bug.”

Practical standards:
1) Pin the *observable contract*, not a computed tautology
- If you assert `expect(extract(a)).toBe(extract(b))` where both sides compute the same fallback that returns `undefined/empty` on many mutations, the test may stay green even when behavior is broken.
- Instead, pin a literal expected output (or a specific substring/field) that only the correct implementation produces.

2) Cover the *actual branch that enforces safety*
- If a guard/invariant exists to prevent silent failure (e.g., “only succeed if either tool-call or file contents are correct”, or skipping when a status is paused, or dedup boundaries), add tests that exercise both the allowed and disallowed combinations.
- Don’t accept broad relaxations like “OR” unless you also assert the missing failure case is still caught.

3) Add boundary and shape variants where logic branches
- For max/min limits, test the exact boundary values (e.g., exactly 8,000 chars / 16,000 UTF-8 bytes) and one value just above.
- For error handling and typed inputs, test the provider’s alternate shapes (e.g., `ApiError`-shaped quota errors vs plain strings).

4) Use an “equivalent mutant” check before escalating severity
- If a mutation cannot be observed given existing invariants/inputs, the test is not a real coverage gap.
- Otherwise, ensure there is a discriminating input that would make the mutation change an observable output.

Example: avoid a vacuous “either/or” success assertion
```ts
// Wrong pattern (can pass on silent tool failure):
expect(toolCall || updated).toBe(true);

// Mutation-effective pattern:
if (toolCall) {
  expect(updated, 'file must update when tool was called').toBe(true);
}
expect(toolCall || updated, 'must succeed via tool-call or correct content').toBe(true);
```

Example: test exact boundaries
```ts
// Instead of only “over limit” and “under limit”, also test equality.
expect(validateReason('x'.repeat(8000))).toBe(true);
expect(validateReason('x'.repeat(8001))).toBe(false);
```

Example: test alternate error shapes
```ts
it('treats ApiError-shaped quota exhaustion as exhausted', () => {
  const err = { error: { code: 429, message: 'quota exhausted', status: 'RESOURCE_EXHAUSTED' } };
  expect(isQuotaExhaustedError(err)).toBe(true);
});
```

Adopt this as a review checklist for the Testing category:
- Would any plausible regression make the test fail? (mutation-effective)
- Is the guard/invariant branch exercised (both sides)?
- Are boundary/type/shape variants covered where code branches?
- Are assertions pinned to literals/fields that uniquely diagnose the failure mode?