---
title: Testing real boundaries
description: When changes affect adapter/process behavior or other runtime boundaries,
  prefer tests that exercise the real boundary while stubbing only the external dependency—not
  brittle internal/system seams. Also keep tests isolated and assert on observable
  behavior rather than incidental formatting.
repository: cline/cline?x=1
label: Testing
language: TypeScript
comments_count: 6
repository_stars: 70861
---

When changes affect adapter/process behavior or other runtime boundaries, prefer tests that exercise the real boundary while stubbing only the external dependency—not brittle internal/system seams. Also keep tests isolated and assert on observable behavior rather than incidental formatting.

Apply this as:
1) Prefer wire/integration tests for adapter wiring
- Use the real adapter/module and stub only true externals (e.g., fetch).
- Assert the externally observable request/response shape.

```ts
// Example pattern: real adapter + stubbed fetch
it('passes through OpenAI transcription wiring', async () => {
  const fetchStub = vi.fn().mockResolvedValue(/* mock OpenAI response */);
  // configure adapter to use stubbed fetch
  const result = await transcribeAudio(
    { /* openai-native config */ },
    { /* request */ },
    { fetch: fetchStub }
  );
  expect(fetchStub).toHaveBeenCalledWith(
    expect.stringContaining('/v1/audio/transcriptions'),
    expect.anything()
  );
  expect(result.transcript).toBe(/* expected */);
});
```

2) Don’t over-mock system seams unless necessary
- If mocking `node:child_process` or PATH shims would be platform-fragile, validate via real execution/behavior (even if it’s more “expensive”).

3) Keep test state isolated
- Use test framework helpers to stub and automatically restore environment.

```ts
it('writes persisted MCP headers', async () => {
  vi.stubEnv('CLINE_MCP_SETTINGS_PATH', settingsPath);
  try {
    const code = await runMcpInstallCommand(/* ... */);
    expect(code).toBe(0);
    // assertions...
  } finally {
    vi.unstubAllEnvs();
  }
});
```

4) Avoid brittle assertions on incidental details
- Don’t assert exact log payload field names/serialization when the code path is already covered by behavior-level server tests; assert the outcome/side effects users rely on.

5) Tighten tests for edge-case semantics
- When fixing logic, update/add tests that lock in the intended rule (e.g., pair start/end behavior and preserve failures/unfinished runs) so regressions can’t reintroduce the ambiguity.
