---
title: Comprehensive coverage collection
description: Configure Jest to collect coverage data from all source files, not just
  those with existing tests, while avoiding test failures due to coverage thresholds.
  Coverage enforcement should be handled by external reporting tools rather than the
  test runner itself.
repository: langflow-ai/langflow
label: Testing
language: JavaScript
comments_count: 2
repository_stars: 111046
---

Configure Jest to collect coverage data from all source files, not just those with existing tests, while avoiding test failures due to coverage thresholds. Coverage enforcement should be handled by external reporting tools rather than the test runner itself.

Use comprehensive `collectCoverageFrom` patterns to include all source files while excluding test files, setup files, and type definitions:

```javascript
module.exports = {
  collectCoverage: true,
  collectCoverageFrom: [
    "src/**/*.{ts,tsx}",
    "!src/**/*.{test,spec}.{ts,tsx}",
    "!src/**/tests/**",
    "!src/**/__tests__/**",
    "!src/setupTests.ts",
    "!src/vite-env.d.ts",
    "!src/**/*.d.ts",
  ],
  // Remove coverageThreshold to avoid test failures
  // Let external tools like codecov handle enforcement
};
```

This approach provides complete visibility into code coverage across the entire codebase while keeping test execution focused on correctness rather than coverage metrics.