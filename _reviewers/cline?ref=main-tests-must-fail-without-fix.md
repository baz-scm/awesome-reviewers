---
title: Tests must fail without fix
description: 'A test is only as good as its ability to catch the regression it claims
  to guard. Before trusting a new or changed test, verify it actually fails when the
  underlying fix is reverted or the behavior is mutated — don''t just confirm it passes
  with the fix in place. Several reviewed tests looked correct but would pass even
  if the bug were reintroduced:'
repository: cline/cline?ref=main
label: Testing
language: TypeScript
comments_count: 8
repository_stars: 70980
---

A test is only as good as its ability to catch the regression it claims to guard. Before trusting a new or changed test, verify it actually fails when the underlying fix is reverted or the behavior is mutated — don't just confirm it passes with the fix in place. Several reviewed tests looked correct but would pass even if the bug were reintroduced:

- An assertion like `value?.should.deepEqual(...)` short-circuits to a pass on `undefined`, silently hiding a dropped field; use `should(value).deepEqual(...)` so a missing value fails loudly.
- A bound like `expect(tokens).toBeLessThan(naive / 10)` only proves "roughly cheaper," not the actual contract; assert the precise, deterministic value instead (e.g., a flat per-image token cost that is identical for a 1-byte and a 500,000-byte payload).
- A cap that was quietly removed (`MAX_CHECKPOINT_FAILURES`) needs a test that fails if the cap is put back, not just one that passes with the current unbounded behavior.
- A plural-catalog validator that strips every CLDR suffix before comparing will pass even when a locale is missing required forms; assert the exact set of expected suffixes instead.
- A test helper that only exercises the common/listed path gives false confidence; explicitly assert the negative case too (e.g., an unlisted model id must not appear in `listModels()`), and confirm the assertion actually bites by pointing it at a case that should fail.

When writing or reviewing a test, ask "would this still pass if the fix were reverted?" Where practical, prove it: revert the change locally, or run a quick mutation (flip a condition, remove a cap, use a different naive comparison) and confirm the test turns red. For behavior with multiple branches or outcome combinations (e.g., every finish-reason × content-type pairing in a retry flow), prefer table-driven tests that cover the full matrix rather than one happy-path case, so no cell can silently regress.