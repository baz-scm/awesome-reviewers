---
title: Verify tests catch regressions
description: A test is only as good as its ability to fail when the behavior it protects
  breaks. Before merging a new or fixed test, confirm it actually fails against the
  pre-fix code (or a deliberately reintroduced bug) and passes against the fix — this
  "mutation" check is as important as the assertion itself. Several bugs slipped through
  specifically because an...
repository: cline/cline?x
label: Testing
language: TypeScript
comments_count: 15
repository_stars: 70983
---

A test is only as good as its ability to fail when the behavior it protects breaks. Before merging a new or fixed test, confirm it actually fails against the pre-fix code (or a deliberately reintroduced bug) and passes against the fix — this "mutation" check is as important as the assertion itself. Several bugs slipped through specifically because an assertion silently no-oped: e.g. `server.tools?.[0].annotations?.should.deepEqual(...)` short-circuits and passes even when `annotations` is `undefined`; rewriting it as `should(server.tools?.[0].annotations).deepEqual(...)` forces the assertion to actually run and fails when the field is dropped. The same discipline applies to fixtures and helpers that could mask the exact defect under test: prefer exercising the real adapter, real catalog, real compiled entrypoint, or a real git/filesystem over a mock that stubs out the very boundary where the bug lives (e.g. testing the real OpenAI-compatible wire format instead of a mocked `@ai-sdk/openai`, or asserting an id is genuinely absent from a live catalog rather than only checking the listed path). When writing a test:
- State in a comment or commit message what buggy behavior the test would have caught, and confirm it fails against that behavior.
- Avoid assertion patterns that can trivially pass (optional chaining before an assertion, loose `toBeTruthy`-style checks, over-permissive regexes/suffix-stripping that hide missing cases).
- Exercise the real implementation/dependency at the seam being tested rather than a mock that could paper over the defect.
- Cover the full round trip and edge cases the code promises (fragments vs. literal `#`, renames carrying old paths, env var cleanup, timing races), not just the common path.
- Keep tests scoped to behavioral guarantees; trim cases that only pin incidental implementation details once the core promises are covered.</description>
</invoke>
