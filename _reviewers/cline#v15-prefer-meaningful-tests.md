---
title: Prefer meaningful tests
description: 'When adding or updating tests, optimize for *high-signal behavior coverage*
  without creating brittle, platform-dependent, or heavy harness code.


  Practical rules:'
repository: cline/cline#v15
label: Testing
language: TypeScript
comments_count: 4
repository_stars: 70877
---

When adding or updating tests, optimize for *high-signal behavior coverage* without creating brittle, platform-dependent, or heavy harness code.

Practical rules:
1) Don’t add test-only plumbing that’s likely to break across platforms or require complex process/mocking setups; if the behavior depends on real CLI/runtime shape, validate it with real integration inputs.
2) Prefer “wire”/adapter-level tests over shallow mocks when the goal is to ensure the real request/response flow is wired correctly. Stub external I/O (e.g., fetch) but keep the adapter path real.
3) Avoid assertions on unstable formatting details (e.g., log payload field names) when the behavior is already covered by existing tests; log-shape tests tend to be brittle and expensive.
4) Keep tests deterministic and isolated: stub the correct method to prevent hanging listeners/streams, and use the test framework’s env stubbing/cleanup to avoid leaking global state.

Example pattern (wire-style):
```ts
// Keep the adapter path real; stub only external I/O.
vi.stubGlobal('fetch', mockFetch);
await transcribeAudio({
  config: { provider: 'openai-native', /* ... */ },
  /* ... */
});
expect(mockFetch).toHaveBeenCalledWith(
  expect.stringContaining('/v1/audio/transcriptions'),
  expect.objectContaining({ method: 'POST' }),
);
```

Example pattern (env hygiene):
```ts
vi.stubEnv({ CLIN_E_MCP_SETTINGS_PATH: settingsPath });
try {
  await runCommand();
} finally {
  vi.unstubAllEnvs();
}
```