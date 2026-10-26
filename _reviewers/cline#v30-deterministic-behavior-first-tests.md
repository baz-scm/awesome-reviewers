---
title: Deterministic, behavior-first tests
description: 'Tests should be (a) behavior-focused, (b) robust across environments,
  and (c) deterministic/isolated.


  Apply these rules:

  - Avoid brittle assertions on implementation details (e.g., exact log payload shapes,
  process-count/zombie counts) unless it provides real behavioral protection.'
repository: cline/cline#v30
label: Testing
language: TypeScript
comments_count: 6
repository_stars: 70894
---

Tests should be (a) behavior-focused, (b) robust across environments, and (c) deterministic/isolated.

Apply these rules:
- Avoid brittle assertions on implementation details (e.g., exact log payload shapes, process-count/zombie counts) unless it provides real behavioral protection.
- Prefer using exported/shared constants instead of hardcoding package/version strings in tests.
- For critical integration/wiring (adapter selection, request routing), prefer wire/adapter-level tests that stub only the external boundary (e.g., fetch), not the whole vendor internals.
- Ensure tests cannot hang or leak resources: stub the correct layer so no never-ending streams/listeners/processes survive past the test.
- Isolate and restore test environment safely: use the test runner’s env stubbing utilities and clean up via their un-stubbing APIs.

Example patterns:
- Environment isolation (Vitest):
```ts
const settingsPath = join(tmpdir(), "settings.json");
vi.stubEnv("CLINE_MCP_SETTINGS_PATH", settingsPath);
try {
  await runCommand(/* ... */);
} finally {
  vi.unstubAllEnvs();
}
```
- Preventing test hangs by stubbing at the correct call site (conceptually):
```ts
const showStub = sandbox.stub();
const terminalInfo = {
  terminal: {
    show: showStub,
    shellIntegration: {
      executeCommand: () => ({ read: () => createNeverEndingStream() }),
    },
  },
};
manager.runCommand(terminalInfo as any, "echo hi");
// Ensure the implementation under test does not attach long-lived listeners or block.
```

Result: fewer flaky tests, less brittle coupling to internals, and faster confidence that critical paths (especially wiring) actually work in production-like conditions.