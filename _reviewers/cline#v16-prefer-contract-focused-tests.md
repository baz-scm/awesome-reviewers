---
title: Prefer contract-focused tests
description: 'When writing tests, keep them behavior/contract focused and self-contained:


  - Avoid brittle harnessing: don’t count spawned processes or mock deep internals
  just to assert implementation details (and avoid platform-specific “test plumbing”
  like shell wrappers).'
repository: cline/cline#v16
label: Testing
language: TypeScript
comments_count: 6
repository_stars: 70882
---

When writing tests, keep them behavior/contract focused and self-contained:

- Avoid brittle harnessing: don’t count spawned processes or mock deep internals just to assert implementation details (and avoid platform-specific “test plumbing” like shell wrappers).
- Don’t assert log payload shapes unless the log fields are an explicit, documented contract; otherwise you’ll need heavy logging harnessing and the test will churn.
- Ensure test determinism and cleanup: stub and restore environment variables using the test framework’s helpers, and stub long-running/async dependencies so no listeners/process activity can outlive the test.
- Tighten spec-based correctness checks: if the feature depends on a standards matrix (e.g., CLDR plural categories), assert completeness rather than letting partial/missing groups silently pass.
- Use shared exported constants in tests to prevent drift (avoid hardcoding values that should come from config/package metadata).

Example (env handling + cleanup):
```ts
import { vi, it, expect } from 'vitest';

it('writes settings using stubbed env', async () => {
  vi.stubEnv('CLINE_MCP_SETTINGS_PATH', '/tmp/test.json');
  try {
    // run code that reads CLINE_MCP_SETTINGS_PATH
    expect(true).toBe(true);
  } finally {
    vi.unstubAllEnvs();
  }
});
```

Example (prevent leaked async behavior via targeted stubbing):
```ts
const runStub = sandbox.stub(VscodeTerminalProcess.prototype, 'run').resolves(/* ... */);
// invoke run
// assertions
runStub.restore();
```