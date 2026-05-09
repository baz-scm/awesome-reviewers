---
title: Isolate process-global mocks
description: When a test uses process-global/irreversible module mocking, prevent
  cross-test contamination by isolating the affected test files into separate `bun
  test` runs (batch isolation). Keep mocks narrowly scoped so tests don’t need to
  mock large dependency graphs, and avoid importing “config/provider” chains in units
  where tests shouldn’t require them.
repository: coleam00/Archon
label: Testing
language: TypeScript
comments_count: 2
repository_stars: 21089
---

When a test uses process-global/irreversible module mocking, prevent cross-test contamination by isolating the affected test files into separate `bun test` runs (batch isolation). Keep mocks narrowly scoped so tests don’t need to mock large dependency graphs, and avoid importing “config/provider” chains in units where tests shouldn’t require them.

Practical checklist:
- Prefer narrow `mock.module()` for the exact dependency that causes nondeterminism (e.g., config derived from developer machine).
- If the runtime mocking mechanism is process-global, run the mocked test(s) in their own `bun test <file>` (or separate script/job) rather than grouping.
- If mocking a dependency would require mocking an entire provider registry, refactor the unit to reduce import chain coupling (e.g., read minimal config directly or inject a loader so the unit under test can be exercised without pulling in the full provider stack).

Example (pattern):
```ts
// conversations.test.ts
mock.module('../config/config-loader', () => ({
  loadConfig: mock(async () => ({ assistant: 'claude' })),
}));
```
Then run it as an isolated invocation:
```bash
cd packages/core && bun test packages/core/src/db/conversations.test.ts
```

This ensures your tests remain deterministic and don’t break due to local `.archon/config.yaml` contents or prior mocked state from other test files.