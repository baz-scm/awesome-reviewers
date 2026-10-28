---
title: Prove tests catch regressions
description: 'A test that merely restates the implementation can pass even when the
  behavior it''s meant to guard is broken. Before marking a test complete, demonstrate
  that it actually fails when the fix or guarded behavior is absent: revert the change
  (or apply a targeted mutation to the production code) and confirm the test goes
  red, then confirm it goes green with the...'
repository: ogulcancelik/herdr#canary966c66ad
label: Testing
language: Rust
comments_count: 6
repository_stars: 46332
---

A test that merely restates the implementation can pass even when the behavior it's meant to guard is broken. Before marking a test complete, demonstrate that it actually fails when the fix or guarded behavior is absent: revert the change (or apply a targeted mutation to the production code) and confirm the test goes red, then confirm it goes green with the fix in place.

Apply this especially to regression tests for subtle bugs (off-by-one rendering, race conditions, reconciliation logic) where it's easy to write an assertion that happens to pass for the wrong reason. For example, a two-workspace test for "closing a tab keeps focus on the right workspace" can pass by coincidence because the survivor's index matches the default fallback; a three-workspace scenario where the survivor's index changes is needed to actually exercise the reconciliation code. Similarly, when fixing an off-by-one in cursor clamping, first confirm the bug reproduces (e.g., text under the clamped caret) before asserting the corrected behavior (a blank cell at the caret).

When feasible, run the test against the unpatched code or a small mutation of the fix and record which specific change makes it fail — this is strong evidence the test targets the right behavior rather than an incidental side effect. Note this check in the PR description or commit message when the bug was subtle.