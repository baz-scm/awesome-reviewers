---
title: Organize tests properly
description: Tests should be well-structured with clear separation of concerns, proper
  grouping, and appropriate cleanup mechanisms. Separate different types of tests
  (performance vs functional), use descriptive test blocks, and ensure proper isolation
  to prevent side effects between tests.
repository: prettier/prettier
label: Testing
language: JavaScript
comments_count: 3
repository_stars: 50772
---

Tests should be well-structured with clear separation of concerns, proper grouping, and appropriate cleanup mechanisms. Separate different types of tests (performance vs functional), use descriptive test blocks, and ensure proper isolation to prevent side effects between tests.

Key practices:
- Separate performance tests from functional tests to avoid environment-dependent failures
- Use nested describe blocks to group related test cases logically
- Implement proper cleanup in finally blocks when tests modify global state
- Structure tests with clear "Invalid usage" and "Valid usage" sections when testing both scenarios

Example structure:
```js
describe("doc builders", () => {
  test("Invalid usage", () => {
    // test invalid scenarios
  });
  test("Valid usage", () => {
    // test valid scenarios  
  });
});

test("node version error", async () => {
  const originalProcessVersion = process.version;
  try {
    Object.defineProperty(process, "version", { value: "v8.0.0" });
    const result = await runPrettier("cli", ["--help"]);
    // assertions
  } finally {
    Object.defineProperty(process, "version", { 
      value: originalProcessVersion 
    });
  }
});
```

This approach prevents test pollution, improves maintainability, and ensures reliable test execution across different environments.