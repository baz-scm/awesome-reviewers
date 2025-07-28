---
title: comprehensive test coverage
description: Ensure tests cover both happy path scenarios and edge cases, including
  error conditions and boundary behaviors. Always wrap test code in proper test functions
  to leverage framework benefits like sanitizers and proper test isolation.
repository: denoland/deno
label: Testing
language: TypeScript
comments_count: 2
repository_stars: 103714
---

Ensure tests cover both happy path scenarios and edge cases, including error conditions and boundary behaviors. Always wrap test code in proper test functions to leverage framework benefits like sanitizers and proper test isolation.

When writing tests, consider potential failure modes and edge cases that could cause crashes or unexpected behavior. For iterative operations, test what happens on subsequent iterations. For resource-intensive operations, ensure proper cleanup and error handling.

Example:
```typescript
Deno.test("[node/sqlite] StatementSync#iterate edge cases", () => {
  const db = new DatabaseSync(":memory:");
  const stmt = db.prepare("SELECT 1 UNION ALL SELECT 2");
  
  // Test normal iteration
  const result1 = [];
  for (const row of stmt.iterate()) {
    result1.push(row);
  }
  
  // Test second iteration (edge case)
  const result2 = [];
  for (const row of stmt.iterate()) {
    result2.push(row);
  }
  
  assertEquals(result1, result2); // Verify consistent behavior
});
```

Always prefer `Deno.test()` wrappers over standalone code to benefit from sanitizers, proper error handling, and test isolation.