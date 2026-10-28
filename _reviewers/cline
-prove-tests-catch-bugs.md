---
title: Prove tests catch bugs
description: A test only has value if it actually fails when the behavior it protects
  is broken. When adding or reviewing a test, demonstrate that it fails against the
  buggy/unfixed code (by temporarily reverting the fix, mutating the implementation,
  or fuzzing invariants) and passes once the fix lands — don't just assert it "should"
  catch the bug.
repository: "cline/cline\r\n"
label: Testing
language: TypeScript
comments_count: 12
repository_stars: 70946
---

A test only has value if it actually fails when the behavior it protects is broken. When adding or reviewing a test, demonstrate that it fails against the buggy/unfixed code (by temporarily reverting the fix, mutating the implementation, or fuzzing invariants) and passes once the fix lands — don't just assert it "should" catch the bug.

This closes several common gaps:
- Avoid assertions that silently pass on missing data, e.g. `value.should.deepEqual(...)` short-circuits when `value` is `undefined`; use `should(value).deepEqual(...)` so a dropped field actually fails the test.
- Prefer exact/strict assertions over loose bounds when the implementation guarantees an exact value (e.g. assert a flat per-item cost equals a constant, not merely "less than some multiple").
- Exercise real code paths instead of over-mocked stand-ins where the mock could hide the actual bug — e.g. a wire-level test against the real HTTP adapter and a stubbed `fetch` catches type/runtime mismatches that a fully mocked unit test cannot; a real git submodule fixture catches tree/blob handling mocks would never exercise.
- For stateful or order-sensitive logic, add both a pinned example sequence and, where practical, a property/fuzz check of the invariants (e.g. "skip hides only its row, undo restores it") run against the buggy version to confirm it can actually detect regressions.
- When removing an artificial limit or cap, add a test that pins the new unbounded behavior and fails if the limit is reintroduced.
- Verify environment/isolation guards (e.g. temp HOME/discovery paths in smoke tests) by running with a hostile value in the surrounding environment and confirming it's untouched.

If a test can't be meaningfully strengthened this way without disproportionate scaffolding for trivial logic already covered elsewhere, it's reasonable to skip it — but say so explicitly rather than adding a test that can't fail.