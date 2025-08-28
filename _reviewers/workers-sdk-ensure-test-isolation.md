---
title: ensure test isolation
description: Tests must be isolated and not leak state between runs. This includes
  properly cleaning up mocks, spies, and any global state modifications to ensure
  reliable and maintainable test suites.
repository: cloudflare/workers-sdk
label: Testing
language: TypeScript
comments_count: 4
repository_stars: 3379
---

Tests must be isolated and not leak state between runs. This includes properly cleaning up mocks, spies, and any global state modifications to ensure reliable and maintainable test suites.

Key practices:
- Configure automatic mock restoration in test setup (e.g., `restoreMocks: true` in Vitest config)
- Reset any modified global state in `afterEach` hooks
- Use explicit test setup rather than relying on shared defaults that might affect other tests
- Collect assertion data in test scope variables rather than using `expect()` inside mocks to improve debuggability

Example of proper cleanup:
```ts
describe("dialog helpers", () => {
  let originalStdoutColumns: number;

  beforeAll(() => {
    originalStdoutColumns = process.stdout.columns;
  });

  afterEach(() => {
    process.stdout.columns = originalStdoutColumns;
  });

  test("with lines truncated", async () => {
    process.stdout.columns = 40;
    // test logic here
  });
});
```

This prevents test pollution where one test's modifications affect subsequent tests, leading to flaky or unreliable test results.