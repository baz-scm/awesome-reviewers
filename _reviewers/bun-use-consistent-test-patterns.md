---
title: Use consistent test patterns
description: Standardize testing by leveraging established patterns and helper functions
  throughout your test suite. Extract repetitive test setup into lifecycle hooks like
  `beforeEach` or shared fixtures. Use existing test helpers rather than duplicating
  logic, and organize tests logically by functionality.
repository: oven-sh/bun
label: Testing
language: TypeScript
comments_count: 4
repository_stars: 79093
---

Standardize testing by leveraging established patterns and helper functions throughout your test suite. Extract repetitive test setup into lifecycle hooks like `beforeEach` or shared fixtures. Use existing test helpers rather than duplicating logic, and organize tests logically by functionality.

For example, instead of repeating server setup in multiple tests:

```javascript
test("test case 1", async () => {
  using server = Bun.serve({
    port: 0,
    async fetch(req, res) { /* ... */ },
  });
  // test logic
});

test("test case 2", async () => {
  using server = Bun.serve({
    port: 0,
    async fetch(req, res) { /* ... */ },
  });
  // test logic
});
```

Prefer using lifecycle hooks:

```javascript
describe("server tests", () => {
  let server;
  
  beforeEach(() => {
    server = Bun.serve({
      port: 0,
      async fetch(req, res) { /* ... */ },
    });
  });
  
  afterEach(() => {
    server.stop();
  });
  
  test("test case 1", async () => {
    // test logic using server
  });
  
  test("test case 2", async () => {
    // test logic using server
  });
});
```

Similarly, use established helper functions (like `fixtureURL`, `itBundled`) for resource loading and specific testing scenarios. Group related tests into logical units and place tests in files that match their functionality. This approach reduces code duplication, improves maintainability, and makes tests easier to understand.