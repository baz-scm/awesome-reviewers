---
title: Pragmatic, Behavior-First Testing
description: 'When adding/changing tests, prefer reliability and behavior coverage
  over brittle instrumentation.


  - Assert observable behavior (outputs, requests/responses, state transitions) rather
  than incidental internals like exact log-field shapes or process-count side effects.'
repository: cline/cline#v10
label: Testing
language: TypeScript
comments_count: 7
repository_stars: 70869
---

When adding/changing tests, prefer reliability and behavior coverage over brittle instrumentation.

- Assert observable behavior (outputs, requests/responses, state transitions) rather than incidental internals like exact log-field shapes or process-count side effects.
- If a unit-test would require heavy, platform-sensitive mocking/harness (e.g., process spawning counts, PATH-wrapped binaries), validate correctness with a higher-level test that exercises the real flow/tooling, using selective stubs only where appropriate.
- Stub at the correct seam to prevent resource leaks/hangs (e.g., stub the process runner rather than providing never-ending streams that keep listeners alive).
- Tighten overly-permissive assertions so invalid data doesn’t slip through; encode real domain rules.
- Use contract/wire tests when correctness depends on version wiring or adapter integration: verify dependency constants match and confirm real adapter request wiring with a stubbed network layer.

Example pattern (behavior over brittle harness):
```ts
// Prefer a wire-style test with the real adapter, but stub fetch.
const fetchStub = sandbox.stub(globalThis, "fetch").resolves(mockResponse);
await transcribeAudio({ /* real openai-native config */ });
expect(fetchStub).toHaveBeenCalledWith(
  expect.stringContaining("/v1/audio/transcriptions"),
  expect.anything(),
);
```
