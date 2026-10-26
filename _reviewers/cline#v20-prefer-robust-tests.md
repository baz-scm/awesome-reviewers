---
title: Prefer robust tests
description: 'Write tests that validate observable behavior with minimal, non-brittle
  harnessing.


  Guidelines:

  - Avoid environment-dependent or implementation-detail “plumbing” mocks (e.g., mocking
  child-process internals or wrapping binaries just to count processes). Prefer existing
  correctness tests or pragmatic real-world checks.'
repository: cline/cline#v20
label: Testing
language: TypeScript
comments_count: 7
repository_stars: 70886
---

Write tests that validate observable behavior with minimal, non-brittle harnessing.

Guidelines:
- Avoid environment-dependent or implementation-detail “plumbing” mocks (e.g., mocking child-process internals or wrapping binaries just to count processes). Prefer existing correctness tests or pragmatic real-world checks.
- Don’t assert on internal/log payload shape unless it’s a true contractual requirement; rely on behavior exercised by existing server/integration tests instead of brittle console/log assertions.
- Keep tests leak-free: stub at the correct boundary so you don’t leave never-ending streams/listeners running past the test.
- When the bug is about integration/adapters, add a wire/integration-style test that drives the real adapter with the smallest possible stub (e.g., stub fetch, then assert the outgoing endpoint and response).
- Prevent “missing coverage” false passes: if completeness matters (e.g., CLDR plural categories), make tests require exact expected groups rather than stripping/ignoring missing variants.
- Use regression tests: reproduce the failure with a failing assertion first, then fix and re-run.

Example pattern (wire test with minimal stubbing):
```ts
// Arrange: drive the real adapter, stub only the network layer
const fetchStub = sandbox.stub(globalThis, 'fetch').resolves(
  new Response(JSON.stringify({ text: 'hello' }), { status: 200 })
);

// Act
const result = await transcribeAudio({
  config: { type: 'openai-native', /* ... */ },
  input: /* ... */,
});

// Assert: validate observable behavior
sinon.assert.calledWithMatch(fetchStub, /\/v1\/audio\/transcriptions/);
expect(result.text).toBe('hello');
```
