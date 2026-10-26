---
title: Prefer Realistic Test Levels
description: When behavior depends on OS/runtime/external processes or cross-layer
  state, write tests that exercise the same integration points (not just helpers)
  and avoid brittle mocks that distort behavior.
repository: cline/cline#v19
label: Testing
language: TypeScript
comments_count: 5
repository_stars: 70885
---

When behavior depends on OS/runtime/external processes or cross-layer state, write tests that exercise the same integration points (not just helpers) and avoid brittle mocks that distort behavior.

Apply:
- Use real adapters/CLIs and stub only the network/IO boundary when possible (e.g., stub `fetch`, but still drive the real adapter request/response).
- If a test would require mocking `child_process`/PATH wrappers, treat it as a signal to move toward an integration-style assertion (validate the observable output/behavior rather than spawn counts).
- For UI/state logic (hooks/coordinators), prefer full rendering/flow tests over helper-only unit tests when the bug is in orchestration/state transitions.
- Add runtime smoke tests for “it starts” regressions by booting the actual binary/daemon in an isolated temp home/data dir, and protect against hostile parent env via explicit isolation.
- Avoid brittle assertions on incidental telemetry/log payload schemas (field-name/format churn). Prefer existing higher-level server/integration tests that cover the real path.

Example pattern:
```ts
// Integration-ish: stub the network boundary, but still run the real adapter.
// (Pseudo-code)
const adapter = createOpenAIRealAdapter(config);
mockFetchToReturn({ transcript: 'hello' });
const res = await transcribeAudio({ adapter, model: 'openai-native' });
expect(res.transcript).toBe('hello');
expect(fetch).toHaveBeenCalledWith(expect.stringContaining('/v1/audio/transcriptions'));
```

Outcome: fewer cross-platform issues, less test brittleness, and coverage that tracks the production failure modes more closely.