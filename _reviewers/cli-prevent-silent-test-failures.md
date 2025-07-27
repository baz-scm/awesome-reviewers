---
title: prevent silent test failures
description: Tests must explicitly fail when expected conditions are not met, rather
  than silently exiting early or using weak assertions that can hide real issues.
  Silent test failures create false confidence in test suites and can mask regressions.
repository: snyk/cli
label: Testing
language: TypeScript
comments_count: 7
repository_stars: 5178
---

Tests must explicitly fail when expected conditions are not met, rather than silently exiting early or using weak assertions that can hide real issues. Silent test failures create false confidence in test suites and can mask regressions.

**Key practices:**

1. **Fail explicitly on missing preconditions**: Instead of early returns, throw errors or use explicit assertions
2. **Use strict assertions**: Prefer exact matches over loose checks like "greater than 0" unless specifically needed
3. **Validate actual content**: Test the substance of outputs, not just their existence
4. **Assert before accessing**: Check conditions before attempting to access files or data structures

**Example of problematic pattern:**
```typescript
it('should create sarif result with ignored issues omitted', async () => {
  const sarifWithoutIgnores = resultWithoutIgnores?.analysisResults.sarif.runs[0].results;
  if (!sarifWithoutIgnores) return; // Silent failure - test passes but validates nothing
  // ... rest of test
});
```

**Better approach:**
```typescript
it('should create sarif result with ignored issues omitted', async () => {
  const sarifWithoutIgnores = resultWithoutIgnores?.analysisResults.sarif.runs[0].results;
  expect(sarifWithoutIgnores).toBeDefined(); // Explicit failure if condition not met
  // ... rest of test with confidence that data exists
});
```

**For output validation:**
```typescript
// Weak - only checks existence
expect(stdoutBuffer).toBeDefined();

// Better - validates actual structure and content
expect(JSON.parse(stdout)).toMatchSchema(expectedSchema);
expect(backendRequests).toHaveLength(2); // Exact expectation, not just > 0
```

This prevents tests from appearing to pass when they're actually not testing anything meaningful.