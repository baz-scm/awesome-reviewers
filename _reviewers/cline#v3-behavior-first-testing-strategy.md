---
title: Behavior-First Testing Strategy
description: When changes are driven by real runtime behavior (process execution,
  adapters, network, logging paths), write tests that verify observable outcomes with
  minimal, stable harnessing.
repository: cline/cline#v3
label: Testing
language: TypeScript
comments_count: 6
repository_stars: 70863
---

When changes are driven by real runtime behavior (process execution, adapters, network, logging paths), write tests that verify observable outcomes with minimal, stable harnessing.

Do:
- Prefer behavior-level assertions over brittle internal details.
  - If correctness depends on adapter wiring, use a wire/integration test with stubbed external I/O (e.g., stub fetch, but exercise the real adapter) and assert the actual request/response.
- Stub only the minimal boundary to keep tests isolated and leak-free.
  - Avoid never-ending streams / long-lived listeners unless you also fully control teardown.
- Reuse existing coverage for already-exercised paths.
  - Don’t add heavy log-shape assertions when existing server tests already cover the code path.
- Keep assertions spec-accurate.
  - Use exported constants (exact versions/packages) rather than hardcoded “latest”.
  - Validate locale-dependent data against formal rules (e.g., required CLDR cardinal categories), not permissive normalization.

Don’t:
- Add cross-platform, test-only plumbing (e.g., child_process mocks that break promise wrappers, PATH shell wrappers) just to count processes when it’s not required for behavioral verification.
- Make permissive checks that allow missing required groups/categories.
- Assert unstable internals (exact log payload fields) when it adds significant harness cost and no behavioral gain.

Example pattern (wire test behavior verification):
```ts
// Stub external transport, but exercise the real adapter wiring.
const fetchStub = vi.fn(async () => ({ ok: true, json: async () => ({ text: "hi" }) }));

await transcribeAudio({
  config: { type: "openai-native", model: "whisper-1" },
  file: someBlob,
  // ...
}, { fetch: fetchStub });

expect(fetchStub).toHaveBeenCalledWith(
  expect.stringContaining("/v1/audio/transcriptions"),
  expect.anything()
);
```

Use this strategy to decide test level:
- Unit tests: isolate a single module surface with minimal stubbing.
- Wire/integration tests: validate adapter/runtime wiring with realistic execution, stubbing only external dependencies.
- Skip new harness assertions when existing tests already exercise the relevant behavior path.