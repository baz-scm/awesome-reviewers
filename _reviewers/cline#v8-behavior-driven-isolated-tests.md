---
title: Behavior-Driven, Isolated Tests
description: 'Write tests that assert observable behavior (not internal implementation
  details) while keeping test state isolated and cleanup-safe.


  Guidelines:

  - Prefer behavior/contract assertions over brittle harnessing (e.g., avoid locking
  down log payload shapes or counting internal process spawns via heavy mocks, unless
  it’s truly the product behavior).'
repository: cline/cline#v8
label: Testing
language: TypeScript
comments_count: 5
repository_stars: 70867
---

Write tests that assert observable behavior (not internal implementation details) while keeping test state isolated and cleanup-safe.

Guidelines:
- Prefer behavior/contract assertions over brittle harnessing (e.g., avoid locking down log payload shapes or counting internal process spawns via heavy mocks, unless it’s truly the product behavior).
- When mocks don’t exercise a code path, add a “wire/integration-style” test that runs the real adapter path with the minimum necessary stubbing (e.g., stub `fetch`, not the adapter internals).
- Scope and clean up everything you override:
  - Use test framework env helpers (e.g., `vi.stubEnv`) and the matching cleanup (`vi.unstubAllEnvs`).
  - Stub the exact seam and ensure any streams/listeners terminate so nothing outlives the test.

Example (scoped env + cleanup):
```ts
import { vi, expect, it } from "vitest";

it("persists settings using env-configured path", async () => {
  const settingsPath = "./tmp/settings.json";
  vi.stubEnv("CLINE_MCP_SETTINGS_PATH", settingsPath);

  try {
    // run command that reads/writes settings
    // expect result and file contents
    expect(true).toBe(true);
  } finally {
    vi.unstubAllEnvs();
  }
});
```

Net effect: tests remain stable across refactors, avoid leaking state across cases, and provide coverage that actually reaches the production logic paths.