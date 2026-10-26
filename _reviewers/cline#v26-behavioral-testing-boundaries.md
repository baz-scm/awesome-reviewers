---
title: Behavioral testing boundaries
description: When adding or updating tests, prefer behavior-focused coverage that
  exercises the real critical path with stable, cross-platform harnessing—while avoiding
  fragile assertions that don’t protect behavior.
repository: cline/cline#v26
label: Testing
language: TypeScript
comments_count: 6
repository_stars: 70893
---

When adding or updating tests, prefer behavior-focused coverage that exercises the real critical path with stable, cross-platform harnessing—while avoiding fragile assertions that don’t protect behavior.

Key practices:
- Use wire/integration tests for wiring bugs: exercise the real adapter/endpoint, but stub external I/O (e.g., fetch) to keep the test deterministic.
- Avoid OS/shell-dependent harnessing or heavy mocking of Node internals. If you need to validate effects, use real artifacts/CLIs/checkpoints rather than inventing wrappers that won’t run on Windows.
- Don’t lock tests to log payload shapes unless logs are a stated contract. If the behavior is already covered by existing server tests, rely on those rather than adding brittle log assertions.
- Prevent hangs/leaks: stub the correct execution boundary (not “feed it a never-ending stream”); ensure listeners/side effects don’t outlive the test.
- Cover tricky edge cases with focused tests, and manage global state (like env vars) via stub/restore helpers.

Example patterns (self-contained):

```ts
// 1) Wire-ish test: real adapter wiring + stubbed network
it('sends audio transcription to the real adapter', async () => {
  const fetchStub = vi.fn().mockResolvedValue(/* ... */);
  globalThis.fetch = fetchStub as any;

  const result = await transcribeAudio({ /* openai-native config */ } as any);
  expect(fetchStub).toHaveBeenCalledWith('/v1/audio/transcriptions', expect.anything());
  expect(result).toMatchObject({ /* transcript */ });
});

// 2) Safe env stubbing
it('persists wizard header settings', async () => {
  vi.stubEnv('CLINE_MCP_SETTINGS_PATH', settingsPath);
  try {
    const code = await runMcpInstallCommand({ /* headers */ } as any);
    expect(code).toBe(0);
    expect(JSON.parse(readFileSync(settingsPath,'utf8')).mcpServers.docs.transport.headers)
      .toEqual({ Authorization: 'Bearer token' });
  } finally {
    vi.unstubAllEnvs();
  }
});

// 3) Deterministic boundary stubbing
it('reveals terminal without taking focus (no hang)', async () => {
  const showStub = sandbox.stub();
  const terminalInfo = { /* terminal: { show: showStub, executeCommand: ... } */ } as any;
  await manager.runCommand(terminalInfo, 'echo hi');
  sinon.assert.calledOnceWithExactly(showStub, true);
});
```

If you follow this, tests stay meaningful (they catch real regressions), deterministic (no hangs/state bleed), and maintainable (not brittle to incidental formatting/log-field changes).