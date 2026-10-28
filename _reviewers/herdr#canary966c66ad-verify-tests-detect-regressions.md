---
title: Verify tests detect regressions
description: A test that always passes is worse than no test at all. Before trusting
  a regression test or an automated verdict, prove it actually fails in the absence
  of the fix or the real-world evidence it's meant to require.
repository: ogulcancelik/herdr#canary966c66ad
label: Testing
language: Python
comments_count: 6
repository_stars: 46332
---

A test that always passes is worse than no test at all. Before trusting a regression test or an automated verdict, prove it actually fails in the absence of the fix or the real-world evidence it's meant to require.

Apply this in two ways:

1. Negative-control the test itself. After writing a test, temporarily reintroduce the bug (revert the fix, stub out the helper being tested, or drop the flag) and confirm the test fails; then restore the fix and confirm it passes. For example, when testing that `git diff --default-prefix` fixes a patch-apply regression, confirm locally that omitting the flag reproduces the original failure (`git apply` error) and that adding it makes the test pass — only then is the regression "locked in." Likewise, when adding tests for shell helper functions, replace the helper with a trivial stub and confirm the new assertions actually fail; if bypassing a helper doesn't break any test, the test suite isn't exercising it.

2. Require positive evidence over assumed success. Verdicts, reports, and classifiers must not default to "pass" when evidence is missing, ambiguous, or incomplete — treat such cases as `inconclusive`/`fail` instead. For example, a clipboard-paste check should fail on a terminal-issued paste and report `inconclusive` (not `pass`) when the trace is absent or ambiguous, rather than assuming a bridge reaction occurred. Aggregate reports should likewise require every planned case/combination to be present and matched before claiming a full pass; a report must never claim "all green" from missing or partial observations.

Finally, avoid multiplying near-duplicate mocked test cases that merely mirror branch literals without exercising distinct real behavior (e.g., don't add separate 404/exhaustion tests that just assert the same mocked branch as an existing dynamic retry test); prefer fewer tests that dynamically prove the behavior under realistic conditions over many that only restate the implementation.