---
title: Verify tests catch the bug
description: 'A test is only as good as its ability to fail when the behavior it covers
  breaks. When adding a regression test, prove it actually detects the defect: temporarily
  revert the fix (or reintroduce the bug) and confirm the new test fails, then confirm
  it passes with the fix in place. This catches assertions that silently short-circuit
  (e.g....'
repository: 'cline/cline#

  zzprobe3b82974b: x'
label: Testing
language: TypeScript
comments_count: 16
repository_stars: 71067
---

A test is only as good as its ability to fail when the behavior it covers breaks. When adding a regression test, prove it actually detects the defect: temporarily revert the fix (or reintroduce the bug) and confirm the new test fails, then confirm it passes with the fix in place. This catches assertions that silently short-circuit (e.g. `value?.should.deepEqual(...)` passing on `undefined` instead of failing — assert on the value directly), fixtures that accidentally strip the signal being tested (e.g. a catalog-completeness check that normalizes away the exact suffixes it should require), and happy-path tests that never actually exercise the edge case in the description.

Prefer exercising real behavior over mocks where feasible — a real temp git repo, a real symlink/submodule, a real compiled entrypoint, a real SSH listing script — since mocks can encode the same wrong assumption as the implementation and hide a bug both share. When a case can't reasonably be tested (e.g. it would require building disproportionate test scaffolding for a few lines of logic already covered elsewhere), say so explicitly and point to the existing coverage, rather than adding a shallow test for its own sake. Likewise, periodically prune tests that only re-verify something already owned and covered by a lower-level component (e.g. detailed telemetry-threading tests duplicating the run loop's own coverage) so the suite's size tracks real risk, not accumulated scaffolding.

Example of the practice in action: for a repo-state parser fix, the regression test used a real temporary git repository, performed the exact operation that used to break (e.g. `git mv`), and asserted the previously-wrong output — and the PR description noted the test fails if the fix is reverted.