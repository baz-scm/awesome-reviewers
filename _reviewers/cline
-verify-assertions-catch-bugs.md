---
title: Verify assertions catch bugs
description: A test only has value if it fails when the behavior it's protecting is
  broken. When writing or reviewing a test, actively confirm this by reverting the
  fix (or imagining the buggy code) and checking the assertion would actually fail
  — don't assume a passing test proves correctness.
repository: 'cline/cline

  '
label: Testing
language: TypeScript
comments_count: 8
repository_stars: 70942
---

A test only has value if it fails when the behavior it's protecting is broken. When writing or reviewing a test, actively confirm this by reverting the fix (or imagining the buggy code) and checking the assertion would actually fail — don't assume a passing test proves correctness.

Watch for these common ways tests pass without really testing anything:
- **Short-circuiting assertions.** `value?.should.deepEqual(expected)` silently no-ops when `value` is `undefined`. Use `should(value).deepEqual(expected)` (or equivalent) so a missing/undefined value fails loudly.
- **Confounded fixtures.** If every fixture for "retry on error code X" also happens to contain a keyword that triggers a separate "retry on message text" check, the code-path for X is never actually exercised in isolation. Vary one dimension at a time (e.g., pair each error code with a neutral message) so each check is independently covered.
- **Loose equivalence checks.** Normalizing away distinctions the real data can have (e.g., stripping all CLDR plural suffixes before comparing keys) can make a catalog missing required plural forms pass undetected. Assert the precise expected shape instead of a relaxed approximation.
- **Over-mocked boundaries.** Mocking the exact module/adapter that contains the real risk (a type-cast across package versions, a wire format) means the mocked test never runs the code that could actually break. Add at least one test that drives the real adapter/dependency (stubbing only the true I/O boundary, e.g. `fetch`) so integration drift is caught.
- **Timing/ordering gaps.** For async coordination (e.g., "does a failed tracked start still let other waiters resolve?"), write the test to start waiting *before* the failure happens, not after, so it can observe the race the implementation must handle.

When an in-process test would require fragile plumbing that doesn't reflect reality (e.g., mocking `child_process` in a way that breaks a promisified API, or wouldn't work cross-platform), it's acceptable to skip the unit test and instead verify against a real-world scenario (real repo, real runtime) and document what was checked and the numbers observed — but don't skip verification entirely.

In all cases, prefer tests that are provably tied to the bug: run them against the broken version to see them fail, then against the fix to see them pass, and note this in the test or PR description.