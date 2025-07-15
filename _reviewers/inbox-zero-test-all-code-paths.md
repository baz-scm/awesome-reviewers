---
title: Test all code paths
description: 'Write comprehensive tests that cover all code paths including edge cases,
  error conditions, and different parameter combinations. Each test file should include:'
repository: elie222/inbox-zero
label: Testing
language: TypeScript
comments_count: 4
repository_stars: 8267
---

Write comprehensive tests that cover all code paths including edge cases, error conditions, and different parameter combinations. Each test file should include:

1. Basic functionality tests
2. Edge case scenarios
3. Error handling cases
4. Different parameter combinations

Example of comprehensive test coverage:

```typescript
describe("findMatchingRule", () => {
  it("handles basic matching", async () => {
    const rule = getRule({ from: "test@example.com" });
    // ... basic test implementation
  });

  it("handles AND operator with multiple conditions", async () => {
    const rule = getRule({
      from: "test@example.com",
      subject: "Important",
      conditionalOperator: LogicalOperator.AND,
    });
    // ... test multiple conditions
  });

  it("handles error conditions", async () => {
    const invalidRule = getRule({ from: null });
    // ... test error handling
  });

  it("handles edge cases", async () => {
    const rule = getRule({
      from: "",
      subject: "".padEnd(1000, "a"), // Very long subject
    });
    // ... test edge cases
  });
});
```

This approach ensures robust code quality by verifying behavior across different scenarios and preventing potential bugs from reaching production.