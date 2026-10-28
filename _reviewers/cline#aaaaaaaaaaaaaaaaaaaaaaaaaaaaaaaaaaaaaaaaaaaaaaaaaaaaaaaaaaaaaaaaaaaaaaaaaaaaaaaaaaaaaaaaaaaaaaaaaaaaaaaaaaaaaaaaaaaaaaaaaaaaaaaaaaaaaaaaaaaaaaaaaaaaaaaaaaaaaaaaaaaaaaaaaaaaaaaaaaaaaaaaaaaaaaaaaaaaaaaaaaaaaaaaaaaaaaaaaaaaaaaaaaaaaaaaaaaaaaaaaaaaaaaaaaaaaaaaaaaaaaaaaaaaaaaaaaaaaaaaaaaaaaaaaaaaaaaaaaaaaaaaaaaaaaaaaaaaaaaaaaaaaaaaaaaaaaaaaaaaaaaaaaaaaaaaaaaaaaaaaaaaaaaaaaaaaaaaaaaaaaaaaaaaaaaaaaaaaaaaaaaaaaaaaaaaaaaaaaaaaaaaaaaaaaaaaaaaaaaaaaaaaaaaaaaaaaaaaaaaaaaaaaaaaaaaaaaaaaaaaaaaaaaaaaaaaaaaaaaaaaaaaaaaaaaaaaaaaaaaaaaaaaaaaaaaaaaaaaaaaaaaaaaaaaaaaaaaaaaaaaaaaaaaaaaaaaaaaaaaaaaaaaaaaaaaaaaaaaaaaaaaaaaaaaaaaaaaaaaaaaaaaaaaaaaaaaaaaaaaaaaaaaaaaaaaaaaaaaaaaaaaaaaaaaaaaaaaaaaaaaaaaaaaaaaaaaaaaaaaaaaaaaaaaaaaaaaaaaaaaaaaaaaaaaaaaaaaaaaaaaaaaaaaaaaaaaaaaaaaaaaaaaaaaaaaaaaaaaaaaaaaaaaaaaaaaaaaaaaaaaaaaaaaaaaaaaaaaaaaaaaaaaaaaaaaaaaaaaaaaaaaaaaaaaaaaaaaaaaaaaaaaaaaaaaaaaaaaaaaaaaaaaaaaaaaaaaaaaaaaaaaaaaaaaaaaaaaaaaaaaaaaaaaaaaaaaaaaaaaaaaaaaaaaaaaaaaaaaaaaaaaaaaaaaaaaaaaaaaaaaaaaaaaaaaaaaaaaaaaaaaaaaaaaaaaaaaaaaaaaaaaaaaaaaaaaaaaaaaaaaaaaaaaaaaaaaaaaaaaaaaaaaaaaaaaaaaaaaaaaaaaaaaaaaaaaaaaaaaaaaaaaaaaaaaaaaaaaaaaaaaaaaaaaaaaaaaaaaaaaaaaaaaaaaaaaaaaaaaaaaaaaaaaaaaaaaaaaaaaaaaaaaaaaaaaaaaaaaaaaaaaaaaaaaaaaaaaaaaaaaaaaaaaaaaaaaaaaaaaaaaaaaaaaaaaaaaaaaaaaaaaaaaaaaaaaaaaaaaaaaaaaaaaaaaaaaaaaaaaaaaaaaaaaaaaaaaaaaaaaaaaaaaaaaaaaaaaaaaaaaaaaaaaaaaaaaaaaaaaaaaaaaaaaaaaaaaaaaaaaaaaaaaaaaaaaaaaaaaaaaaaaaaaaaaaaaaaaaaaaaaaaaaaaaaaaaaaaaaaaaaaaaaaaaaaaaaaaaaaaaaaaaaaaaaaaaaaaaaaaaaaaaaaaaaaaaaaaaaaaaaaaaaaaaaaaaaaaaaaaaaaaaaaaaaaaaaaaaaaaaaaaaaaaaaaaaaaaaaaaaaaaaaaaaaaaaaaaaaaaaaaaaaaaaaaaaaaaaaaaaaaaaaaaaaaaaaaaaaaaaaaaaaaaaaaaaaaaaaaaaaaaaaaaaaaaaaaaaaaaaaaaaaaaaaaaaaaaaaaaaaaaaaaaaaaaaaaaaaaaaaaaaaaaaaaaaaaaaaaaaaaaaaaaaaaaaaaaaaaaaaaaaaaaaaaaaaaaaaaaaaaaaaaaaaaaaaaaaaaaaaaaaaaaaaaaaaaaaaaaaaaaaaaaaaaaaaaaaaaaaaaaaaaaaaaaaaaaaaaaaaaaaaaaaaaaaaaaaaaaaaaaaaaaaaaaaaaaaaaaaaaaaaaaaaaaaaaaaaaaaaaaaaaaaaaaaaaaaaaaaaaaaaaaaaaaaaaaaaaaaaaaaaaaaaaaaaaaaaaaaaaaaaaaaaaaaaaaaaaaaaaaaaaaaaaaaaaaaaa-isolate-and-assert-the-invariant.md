---
title: Isolate and assert the invariant
description: 'Write tests that pin down the exact behavior under test, not a correlated
  proxy, and that accurately document their own scope.


  - Vary only the dimension under test. If every fixture shares an incidental property
  (e.g. all "overloaded" messages also carry the error code being tested), the test
  can pass even when the code-only path is broken. Add cases that...'
repository: cline/cline#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
label: Testing
language: TypeScript
comments_count: 9
repository_stars: 70965
---

Write tests that pin down the exact behavior under test, not a correlated proxy, and that accurately document their own scope.

- Vary only the dimension under test. If every fixture shares an incidental property (e.g. all "overloaded" messages also carry the error code being tested), the test can pass even when the code-only path is broken. Add cases that hold everything else neutral and change just the field in question (plus an "unknown value" case that must stay negative).
- Assert the real invariant directly instead of a loose bound that merely happens to hold. Prefer `expect(perImage).toBe(FLAT_RATE)` over `expect(total).toBeLessThan(someMultiple)`; a direct equality on a flat per-unit cost, computed from two payload sizes 500,000 chars apart, catches a regression that a "less than 10x" bound would miss.
- Clean up test doubles and environment state so one test cannot leak into another: stub at the right layer (don't hand a never-ending stream to a real process when stubbing the process's `run` method avoids leaking listeners), use `vi.stubEnv`/`vi.unstubAllEnvs` instead of manual save/restore of `process.env`, and reset call counts on hoisted mocks in `beforeEach`.
- Keep test comments and descriptions precise about what is and isn't exercised — if a claim like "no assertion depends on the catalog" is only true for some branches, name the test for exactly what it checks instead of overstating independence.
- Scope each test to the layer it actually owns. Don't duplicate a vendored dependency's own behavior (e.g. a shape only `@ai-sdk/amazon-bedrock` controls) in your wrapper's suite, and don't add a redundant case that risks colliding with real-world state (e.g. a default port) when an isolated unit test already covers the same branch elsewhere. When trimming extra cases, keep the ones that cover the feature's core promises (success, failure, no-op) and drop ones that re-verify a lower layer's contract.

Example of isolating the variable:
```ts
it("charges a flat ESTIMATED_TOKENS_PER_IMAGE per image, independent of payload length", () => {
  const estimate = (data: string) =>
    estimateRequestInputTokens({ messages: [{ role: "user", content: [{ type: "image", data, mediaType: "image/png" }] }] });

  expect(estimate("A".repeat(500_000))).toBe(estimate("A"));
  const perImage = estimate("A") - estimateRequestInputTokens({ messages: [{ role: "user", content: [] }] });
  expect(perImage).toBe(ESTIMATED_TOKENS_PER_IMAGE);
});
```