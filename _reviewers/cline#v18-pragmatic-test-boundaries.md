---
title: Pragmatic Test Boundaries
description: Write tests at the behavior/contract boundary, using real implementations
  when mocks would be brittle, and avoid harness-level assertions that couple tests
  to logging or internals.
repository: cline/cline#v18
label: Testing
language: TypeScript
comments_count: 7
repository_stars: 70884
---

Write tests at the behavior/contract boundary, using real implementations when mocks would be brittle, and avoid harness-level assertions that couple tests to logging or internals.

Guidelines:
- Pick the right test layer:
  - Use a **wire/integration test** when the correctness depends on adapter wiring (e.g., the real HTTP path) while **stubbing external I/O** (e.g., fetch).
  - Use **unit tests** for pure logic invariants/edge cases (e.g., pairing start/end events, ensuring failures/unfinished work isn’t dropped).
- Avoid platform-fragile plumbing:
  - Don’t introduce OS-dependent wrappers or mocks that require complex shims (e.g., child-process mocking that breaks executors, shell-script tools not working on Windows).
- Stub the correct boundary and prevent async leaks:
  - Stub the method that would start external work (rather than feeding never-ending streams) so no listeners/processes outlive the test.
- Assert source-of-truth invariants:
  - When exporting constants/versions, test them against the upstream package definition.
  - For domain rules (e.g., i18n/plurals), assert the full required set for the locale categories.
- Don’t add brittle log-shape tests:
  - If the existing server/path tests already exercise the behavior, prefer that over enabling logging and asserting exact payload fields.

Example (wire-style contract test):
```ts
it("sends requests through the real adapter", async () => {
  const fetchStub = vi.fn(async () => ({
    ok: true,
    json: async () => ({ text: "hi" }),
  }));

  // Real adapter used; only external I/O is stubbed.
  const result = await transcribeAudio({
    config: { type: "openai-native" },
    audio: new Uint8Array([0x00]),
    fetch: fetchStub,
  });

  expect(fetchStub).toHaveBeenCalledWith(
    expect.stringContaining("/v1/audio/transcriptions"),
    expect.any(Object)
  );
  expect(result.text).toBe("hi");
});
```