---
title: Verify tests detect regressions
description: A test only has value if it actually fails when the behavior it protects
  breaks. When adding or reviewing a test, confirm this by deliberately reverting
  the fix, removing the guard, or reintroducing the bug, and checking the test turns
  red; note this verification in the PR/commit so reviewers don't have to re-derive
  it.
repository: cline/cline#&&sleep 4
label: Testing
language: TypeScript
comments_count: 10
repository_stars: 70980
---

A test only has value if it actually fails when the behavior it protects breaks. When adding or reviewing a test, confirm this by deliberately reverting the fix, removing the guard, or reintroducing the bug, and checking the test turns red; note this verification in the PR/commit so reviewers don't have to re-derive it.

This also means writing assertions precise enough to catch the real failure mode, not just ones that happen to pass:
- Avoid short-circuiting or optional-chaining assertions on possibly-undefined values (e.g. `value?.should.deepEqual(...)`, which silently skips when `value` is `undefined`). Use a form that fails loudly instead (`should(value).deepEqual(...)`).
- Prefer exact-value or exact-shape checks over loose bounds when an exact value is knowable (e.g. assert a flat `ESTIMATED_TOKENS_PER_IMAGE` per image instead of only `toBeLessThan(naiveEstimate / 10)`), and add the complementary check that payload size doesn't move the result at all.
- Don't let test helpers quietly strip away the cases you need to cover (e.g. collapsing CLDR plural suffixes before comparing keys hid missing `_few`/`_many` entries); make the helper enforce completeness instead of normalizing it away.
- When a fix removes an arbitrary cap or changes a policy, add a test that encodes the new invariant (e.g. "every failure record persists, none are evicted") so the test fails if the old limiting behavior is reintroduced.
- When a value is sourced from configuration (a package version, a CLI constant), assert it against the authoritative source (e.g. `package.json`) rather than duplicating a literal that can drift out of sync.

Treat "I added a test" as incomplete until you've shown, even if only locally, that the test fails against the buggy version and passes against the fix.