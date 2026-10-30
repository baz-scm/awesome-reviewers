---
title: Verify tests catch regressions
description: 'A test is only as good as its ability to fail when the bug it targets
  is present. When writing or reviewing a test, confirm this explicitly rather than
  assuming it:'
repository: cline/cline#"><b>zze3729958
label: Testing
language: TypeScript
comments_count: 9
repository_stars: 71067
---

A test is only as good as its ability to fail when the bug it targets is present. When writing or reviewing a test, confirm this explicitly rather than assuming it:

- Exercise the real implementation, not a copy of its logic. A test that hardcodes the same mapping or computation the code under test uses (e.g. a literal `codePageMap` duplicating what `getWindowsConsoleEncoding()` does internally) will pass even if the real function is wrong. Import and call the real function instead.
- Use assertions that cannot silently no-op. Optional chaining before an assertion (`value?.should.deepEqual(...)`) short-circuits to a pass when the value is `undefined`; wrap the full value (`should(value).deepEqual(...)`) so a missing or dropped field fails the test.
- Isolate the specific condition under test. If every fixture for a "retryable by message content" case also happens to be "retryable by error code," the code-only branch is never actually exercised; add a fixture with a neutral message and the code alone (and the inverse: an unknown code with the same message) so each branch is independently covered.
- Make validation strict, not permissive. A helper that strips all plural suffixes before comparing keys will pass even if a locale's catalog is missing required CLDR categories; assert the exact required set instead of a loosely normalized one.
- Prefer deterministic proof over inline reasoning: fuzz random sequences against the invariant the fix establishes, or write the regression test first and run it against the pre-fix code to confirm it fails with the reported error, then confirm it passes after the fix.
- For boundary/limit logic (truncation, clipping, capacity checks), add a case that pins the exact boundary (e.g., a value at the limit vs. one past it) rather than only testing comfortably inside or outside the range.
- For multi-branch or multi-outcome logic (e.g., every finish-reason × content-shape combination), use a table-driven test covering the full matrix so no cell is silently skipped, especially where a dropped case could mean silently losing data.

Before considering a test complete, revert the fix locally (or reason through the diff) and confirm the test actually fails for the right reason — not because of an unrelated assertion, and not passing by coincidence.