---
title: Prove tests catch regressions
description: 'A test is only as good as its ability to fail when the behavior it protects
  breaks. For every new or modified test, confirm this directly: run it against the
  pre-fix code (or a deliberately broken version) and verify it fails with the expected
  reason, then confirm it passes with the fix. Don''t settle for a test that merely
  exercises the code path — assert...'
repository: cline/cline#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
label: Testing
language: TypeScript
comments_count: 15
repository_stars: 70964
---

A test is only as good as its ability to fail when the behavior it protects breaks. For every new or modified test, confirm this directly: run it against the pre-fix code (or a deliberately broken version) and verify it fails with the expected reason, then confirm it passes with the fix. Don't settle for a test that merely exercises the code path — assert the exact value or behavior at stake, not a loose approximation that would pass even with a wrong implementation.

Concretely:
- Prefer precise assertions over weak ones. `should(value).deepEqual(...)` fails on `undefined`; a bare truthy check or `toBeLessThan` with a generous margin can silently pass even when the feature is broken or absent. When possible, assert the exact expected value (e.g. "costs exactly ESTIMATED_TOKENS_PER_IMAGE per image, independent of payload length") rather than "costs less than some loose bound."
- When a bug lives at an integration boundary (a real SDK, a real adapter, a real git repository, a real compiled entrypoint, wire-level request/response), write at least one test that drives the real dependency end-to-end instead of a mock that would hide the exact mismatch (e.g. type incompatibilities between pinned versions, header hand-off, retry/backoff timing).
- Explicitly test negative and absence cases (a helper that must *not* be called, an id that must *not* appear in a list, a flag that must remain unset) rather than only the positive path.
- Guard derived/duplicated values against drift by asserting they match their single source of truth (e.g. an exported constant equals the value in `package.json`), and verify a hardcoded stand-in would fail that check.
- When adding coverage for a fix, state (in the PR/commit or test comment) how you validated the test actually catches the bug — e.g. "fails with `AssertionError: ...` before the fix, passes after" — so reviewers don't have to take efficacy on faith.

Example of tightening a weak assertion:
```ts
// Before: silently passes if `annotations` is undefined.
server.tools?.[0].annotations?.should.deepEqual({ ... })

// After: fails loudly on undefined.
should(server.tools?.[0].annotations).deepEqual({ ... })
```