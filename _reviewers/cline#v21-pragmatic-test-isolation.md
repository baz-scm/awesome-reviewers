---
title: Pragmatic Test Isolation
description: 'Write tests that validate the *real behavior* without brittle harnessing.
  Concretely:


  - Prefer wire/integration coverage when correctness depends on runtime wiring (adapter
  → HTTP, CLI → wizard parsing, etc.). Stub only the true external boundary (e.g.,
  fetch), but execute the real adapter path.'
repository: cline/cline#v21
label: Testing
language: TypeScript
comments_count: 6
repository_stars: 70886
---

Write tests that validate the *real behavior* without brittle harnessing. Concretely:

- Prefer wire/integration coverage when correctness depends on runtime wiring (adapter → HTTP, CLI → wizard parsing, etc.). Stub only the true external boundary (e.g., fetch), but execute the real adapter path.
- Avoid brittle assertions that couple to implementation details like process counts or log field shapes. If a behavioral path is already exercised by server/integration tests, don’t re-test telemetry payloads.
- Keep unit tests isolated and non-leaky: stub the smallest required method(s) and avoid constructs that spawn listeners/streams that can outlive the test.
- Use your test framework’s environment helpers (e.g., `vi.stubEnv` / `vi.unstubAllEnvs`) rather than manual save/restore that can leave inconsistent state.
- When tests verify cross-package contracts, reference exported source-of-truth constants and assert strict constraints (e.g., exact versions) to prevent drift.

Example pattern (wire test with stubbed external I/O):
```ts
// Pseudocode pattern
mockGlobalFetch((req) => {
  expect(req.url).toBe("/v1/audio/transcriptions");
  return Promise.resolve({ ok: true, json: async () => ({ text: "hi" }) });
});

await transcribeAudio({
  // use real adapter config
  config: "openai-native",
  // assertions verify real wiring via observed request/response
});
```

Apply this as a checklist: “real path first, minimal stubs, no brittle coupling, correct env handling, and source-of-truth constants.”