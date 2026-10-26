---
title: Brittle Test Avoidance
description: 'When adding or updating tests, keep them deterministic and meaningful
  without introducing brittle, platform-sensitive harnessing.


  Practical rules:

  1) Prefer the “right boundary” for stubbing/mocking'
repository: cline/cline#x
label: Testing
language: TypeScript
comments_count: 6
repository_stars: 70861
---

When adding or updating tests, keep them deterministic and meaningful without introducing brittle, platform-sensitive harnessing.

Practical rules:
1) Prefer the “right boundary” for stubbing/mocking
- Stub at the component boundary you control, not by simulating whole processes with never-ending streams or heavy child-process behavior.
- Avoid mocks/wrappers that change execution semantics differently on Windows/macOS/Linux.

2) Don’t assert implementation/log payload shape unless it’s the product contract
- If existing tests already exercise the functional path (e.g., server close/heartbeat behavior), don’t add a logging-shape assertion that requires enabling global logging and console spying.

3) Make environment/state deterministic using test utilities
- Use the test runner’s env stubbing helpers and ensure restoration semantics match “unset vs set”. Don’t manually mutate process.env without proper cleanup.

4) Make helpers strict enough to catch missing/incorrect semantics
- Avoid over-broad normalization that can hide real defects (e.g., plural-category validation that would pass even when required groups are missing).
- Include edge cases that reflect real CLI/input behavior (e.g., literal path handling for patterns like draft*.txt).

5) Prefer real-behavior assertions when mocking would distort meaning
- If the only way to “count” behavior is to mock something that breaks real execution semantics, use real checkpoints/fixtures and assert correctness via existing functional tests.

Example pattern (env determinism):
```ts
import { vi } from "vitest";

it("writes settings for provided headers", async () => {
  const settingsPath = "/tmp/.../cline_mcp_settings.json";
  vi.stubEnv("CLINE_MCP_SETTINGS_PATH", settingsPath);

  try {
    const code = await runMcpInstallCommand({ /* ... */ });
    expect(code).toBe(0);
  } finally {
    vi.unstubAllEnvs(); // correct restore even when the var was unset
  }
});
```

Adopting these rules will reduce flaky tests, prevent leaked listeners/hangs, and ensure failures correspond to real behavioral regressions—not harness artifacts or incidental logging changes.