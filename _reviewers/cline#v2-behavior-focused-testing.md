---
title: Behavior-Focused Testing
description: When writing/adjusting tests, prefer stable, observable behavior assertions
  over brittle “implementation detail” checks, and avoid test harness complexity that
  can vary by platform.
repository: cline/cline#v2
label: Testing
language: TypeScript
comments_count: 6
repository_stars: 70861
---

When writing/adjusting tests, prefer stable, observable behavior assertions over brittle “implementation detail” checks, and avoid test harness complexity that can vary by platform.

Practical rules:
- **Don’t assert log payload shapes** (field names/extra context) unless downstream behavior depends on them. If a behavioral path already has server integration coverage, rely on that instead of adding a logging harness.
- **Avoid heavy mocking that breaks platform behavior.** If verifying internal process counts requires fragile mocks that vary on Windows/Linux, validate correctness via existing real-data coverage or stable functional outcomes.
- **Stub the correct boundary and prevent leaks.** Ensure background listeners/processes created by the unit under test are not left running; if needed, stub the method that drives the long-running behavior.
- **Use the test runner’s env/state utilities correctly** so “unset vs set” is handled safely and restored deterministically.
- **Make helpers strict enough to catch missing cases.** Don’t over-sanitize inputs/results in ways that let regressions slip (e.g., collapsing plural groups in a way that hides missing CLDR categories).

Example pattern (non-brittle vs harness-heavy):
```ts
// Instead of asserting exact log payload structure, rely on the existing
// socket/server behavioral tests that exercise the close path.
// Keep the new test focused on behavior: whether the code path runs and
// observable state changes occur.
```

Apply this by asking: “What externally observable behavior would break in a real regression?” If the answer is “only the exact string/log fields,” that’s usually a sign the test should be rewritten or removed in favor of behavior-focused coverage.