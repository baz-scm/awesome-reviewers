---
title: Use runServerless utility
description: All new tests must be written using the `runServerless` utility instead
  of legacy testing approaches. This utility provides a more reliable way to test
  functionality by replicating full command runs, ensuring that cross-dependent machinery
  works as expected in production.
repository: serverless/serverless
label: Testing
language: JavaScript
comments_count: 25
repository_stars: 46810
---

All new tests must be written using the `runServerless` utility instead of legacy testing approaches. This utility provides a more reliable way to test functionality by replicating full command runs, ensuring that cross-dependent machinery works as expected in production.

The `runServerless` approach offers several advantages:
- Tests the complete integration rather than isolated components
- Reduces maintenance burden during refactors
- Provides consistent testing patterns across the codebase
- Eliminates the need for complex mocking setups

When writing new tests, use `runServerless` with appropriate fixtures and configuration:

```javascript
it('should handle function configuration correctly', async () => {
  const { cfTemplate, awsNaming } = await runServerless({
    fixture: 'function',
    command: 'package',
    configExt: {
      functions: {
        basic: {
          handler: 'index.handler',
          memorySize: 512,
        },
      },
    },
  });
  
  const functionResource = cfTemplate.Resources[awsNaming.getLambdaLogicalId('basic')];
  expect(functionResource.Properties.MemorySize).to.equal(512);
});
```

Do not expand or modify existing legacy tests - they should remain intact or be completely replaced. For test efficiency, consider consolidating multiple test scenarios into a single `runServerless` call when testing related functionality, as these runs are expensive and can prolong test execution time.