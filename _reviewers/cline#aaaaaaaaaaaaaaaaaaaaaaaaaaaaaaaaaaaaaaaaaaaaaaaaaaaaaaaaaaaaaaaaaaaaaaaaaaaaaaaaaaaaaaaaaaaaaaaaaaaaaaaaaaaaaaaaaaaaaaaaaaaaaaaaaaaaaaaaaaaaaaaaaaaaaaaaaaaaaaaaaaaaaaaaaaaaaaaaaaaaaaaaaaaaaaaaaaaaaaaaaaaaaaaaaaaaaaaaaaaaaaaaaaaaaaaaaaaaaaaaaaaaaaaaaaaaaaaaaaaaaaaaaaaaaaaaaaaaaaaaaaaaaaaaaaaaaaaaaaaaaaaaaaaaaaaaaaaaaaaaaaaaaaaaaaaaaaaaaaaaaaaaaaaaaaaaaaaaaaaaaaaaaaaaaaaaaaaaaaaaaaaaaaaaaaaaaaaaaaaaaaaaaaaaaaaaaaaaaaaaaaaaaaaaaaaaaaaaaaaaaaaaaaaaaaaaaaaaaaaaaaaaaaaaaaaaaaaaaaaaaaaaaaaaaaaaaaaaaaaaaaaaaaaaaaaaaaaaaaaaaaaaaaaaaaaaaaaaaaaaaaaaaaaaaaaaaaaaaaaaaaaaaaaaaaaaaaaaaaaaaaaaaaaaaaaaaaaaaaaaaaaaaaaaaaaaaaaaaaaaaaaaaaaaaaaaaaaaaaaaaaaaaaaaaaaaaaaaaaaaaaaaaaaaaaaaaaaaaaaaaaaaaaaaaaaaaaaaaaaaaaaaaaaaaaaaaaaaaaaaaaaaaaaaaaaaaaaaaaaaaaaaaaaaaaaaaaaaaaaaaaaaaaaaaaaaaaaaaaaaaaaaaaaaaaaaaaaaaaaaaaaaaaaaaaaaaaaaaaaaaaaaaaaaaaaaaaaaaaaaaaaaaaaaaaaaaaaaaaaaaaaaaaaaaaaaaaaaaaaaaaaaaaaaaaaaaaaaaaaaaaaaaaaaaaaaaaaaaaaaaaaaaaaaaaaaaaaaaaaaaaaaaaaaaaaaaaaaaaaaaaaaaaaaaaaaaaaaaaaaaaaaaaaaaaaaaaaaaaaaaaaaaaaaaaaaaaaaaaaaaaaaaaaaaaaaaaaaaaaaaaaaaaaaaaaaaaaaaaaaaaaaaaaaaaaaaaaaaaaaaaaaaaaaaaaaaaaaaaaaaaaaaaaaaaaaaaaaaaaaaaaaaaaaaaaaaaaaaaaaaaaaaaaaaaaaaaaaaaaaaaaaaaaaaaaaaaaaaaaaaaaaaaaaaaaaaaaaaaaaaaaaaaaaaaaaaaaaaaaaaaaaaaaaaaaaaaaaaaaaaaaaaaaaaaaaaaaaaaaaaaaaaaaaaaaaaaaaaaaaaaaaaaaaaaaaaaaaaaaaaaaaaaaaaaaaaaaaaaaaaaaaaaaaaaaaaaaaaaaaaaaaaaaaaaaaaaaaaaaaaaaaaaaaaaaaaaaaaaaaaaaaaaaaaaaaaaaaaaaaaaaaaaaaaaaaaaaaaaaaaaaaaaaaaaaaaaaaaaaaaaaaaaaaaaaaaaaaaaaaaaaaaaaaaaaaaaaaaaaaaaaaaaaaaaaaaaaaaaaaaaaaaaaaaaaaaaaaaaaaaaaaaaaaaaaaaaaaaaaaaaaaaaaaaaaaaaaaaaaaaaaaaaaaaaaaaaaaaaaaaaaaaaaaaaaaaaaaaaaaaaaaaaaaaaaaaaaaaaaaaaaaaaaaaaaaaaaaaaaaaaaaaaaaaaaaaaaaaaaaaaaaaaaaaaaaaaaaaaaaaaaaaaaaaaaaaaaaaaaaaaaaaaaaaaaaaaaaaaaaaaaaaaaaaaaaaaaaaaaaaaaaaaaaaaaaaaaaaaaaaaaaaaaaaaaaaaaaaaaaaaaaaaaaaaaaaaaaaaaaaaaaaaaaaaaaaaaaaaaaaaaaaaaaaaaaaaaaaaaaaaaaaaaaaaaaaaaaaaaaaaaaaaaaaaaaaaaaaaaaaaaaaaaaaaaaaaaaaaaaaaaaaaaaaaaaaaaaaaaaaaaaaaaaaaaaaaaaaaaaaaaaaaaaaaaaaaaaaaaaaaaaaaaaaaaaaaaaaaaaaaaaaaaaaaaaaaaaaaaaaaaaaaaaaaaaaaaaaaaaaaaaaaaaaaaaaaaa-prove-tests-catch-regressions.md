---
title: Prove tests catch regressions
description: 'A test is only as good as its ability to fail when the behavior it protects
  breaks. Across many reviews, tests looked complete but did not actually exercise
  the failure they were meant to guard against: an assertion silently short-circuited
  on `undefined` instead of failing, a fixture confounded the one condition under
  test with an unrelated signal that was...'
repository: cline/cline#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
label: Testing
language: TypeScript
comments_count: 13
repository_stars: 70976
---

A test is only as good as its ability to fail when the behavior it protects breaks. Across many reviews, tests looked complete but did not actually exercise the failure they were meant to guard against: an assertion silently short-circuited on `undefined` instead of failing, a fixture confounded the one condition under test with an unrelated signal that was always present (e.g. every "overloaded" case also had "overloaded" in its message, so the error-code check alone was never exercised), a lenient flattening helper stripped away exactly the data (locale plural suffixes) whose absence should have failed the test, or a mock replaced so much of the real system that it stopped reflecting actual behavior.

When writing or reviewing a test:
- Write the assertion so it fails on the wrong value, not just on an exception or a missing field (use `should(value)`, not a chained `.should` on a possibly-`undefined` expression).
- Vary only the one thing you are testing; keep every other input neutral so a case can't pass for the wrong reason (e.g. test an error code with a generic message, separately from testing message-text matching).
- Prefer real/integration-level exercises (real SDK + real wire format, real subprocess entrypoint, real repo operations) over deep mocks that can drift from actual behavior, and when stubbing is necessary, stub at the API boundary rather than low-level internals that can leak resources or miss real control flow.
- Explicitly verify new tests by reverting the fix (or deliberately reintroducing the bug) and confirming the test fails; for probabilistic or invariant-style properties, consider mutation testing or fuzzing to confirm failure modes are caught.
- Cover the edge cases surfaced in review (tab-containing filenames, binary content appearing on either side of a diff, renames/copies, missing required fields, numeric vs string types) with dedicated cases rather than relying on the happy path to imply coverage.
- Remove test setup and assertions that no longer protect anything (unused mock recordings, telemetry-detail tests that duplicate coverage already owned elsewhere) so the suite stays a signal of real risk rather than incidental implementation detail.

Example of fixing a confounded fixture:
```ts
// Before: every case has "overloaded" in the message, so the code check
// alone is never exercised in isolation.
it("retries an overloaded payload", () => { ... message: "... overloaded ..." ... });

// After: table-driven, with a neutral message per code, plus an unknown
// code with a neutral message that must stay non-retryable.
it.each(capacityCodes)("retries %s with a neutral message", (code) => {
  expect(isRetryableProviderError({ error: { code, message: "temporary issue" } })).toBe(true);
});
it("does not retry an unknown code with a neutral message", () => {
  expect(isRetryableProviderError({ error: { code: "unknown_error", message: "temporary issue" } })).toBe(false);
});
```