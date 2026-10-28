---
title: Prove tests catch real regressions
description: Favor tests that exercise real behavior over ones that only assert against
  mocks, and confirm each test actually detects the bug or regression it claims to
  guard against.
repository: cline/cline#$(sleep 4)
label: Testing
language: TypeScript
comments_count: 16
repository_stars: 70978
---

Favor tests that exercise real behavior over ones that only assert against mocks, and confirm each test actually detects the bug or regression it claims to guard against.

- Drive integration points through the real dependency when it's feasible: the real AI SDK adapter with a stubbed `fetch` (wire-contract tests for OpenAI/Bedrock reasoning fields, streaming retry/backoff, transcription), a real temp git repository for source-control parsing (renames, copies, symlinks), a real POSIX script for remote directory listing. A test that mocks the exact boundary it's supposed to validate (e.g. mocking `@ai-sdk/openai` for a hand-off that only runs through the real adapter) can pass while the real integration is broken.
- Before trusting a new or fixed test, verify it actually fails without the fix and passes with it — run it against the old code, or fuzz a wide range of inputs/verb sequences, to be confident the assertion is meaningful rather than vacuously true. Add a control case when needed to prove the scenario you're testing is real (e.g. a short-timeout dispatcher proving the server really does go idle long enough to matter).
- Cover the edge cases that motivated the change explicitly, not just the happy path: boundary values (flat per-item cost independent of payload size), malformed/legacy data shapes, concurrent/disconnected actors, and "what if nothing changed" sanity checks, each phrased as its own assertion.
- When a test's assertion is weaker than the real invariant (e.g. stripping CLDR plural suffixes so a catalog missing required forms still passes), tighten it so it actually enforces the invariant going forward.

Example pattern to follow — pin behavior through the real adapter, not a mock:
```ts
it("does not ask a model without a reasoning-off setting to turn reasoning off", async () => {
  const body = await wireBody({ modelId: "gpt-6-astra", reasoning: { enabled: false } });
  expect((body.reasoning as { effort?: string })?.effort).not.toBe("none");
});
```
and confirm it fails on the old adapter version / without the fix before merging.