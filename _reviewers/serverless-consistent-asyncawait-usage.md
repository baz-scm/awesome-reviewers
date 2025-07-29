---
title: consistent async/await usage
description: When refactoring code to use async/await, ensure complete and consistent
  adoption throughout the function or module. Avoid mixing async/await syntax with
  .then() chains, as this creates confusing and hard-to-maintain code.
repository: serverless/serverless
label: Concurrency
language: JavaScript
comments_count: 9
repository_stars: 46810
---

When refactoring code to use async/await, ensure complete and consistent adoption throughout the function or module. Avoid mixing async/await syntax with .then() chains, as this creates confusing and hard-to-maintain code.

The pattern to avoid:
```javascript
// Bad: mixing async/await with .then()
async function example() {
  const result = await someAsyncOperation();
  return result.then(data => processData(data));
}

// Bad: using .then() after await
await expect(awsPlugin.monitorStack('update', cfData, { frequency: 10 }))
  .to.eventually.be.rejectedWith(ServerlessError, 'An error occurred')
  .then(() => {
    // additional logic
  });
```

The preferred approach:
```javascript
// Good: consistent async/await
async function example() {
  const result = await someAsyncOperation();
  const processedData = await processData(result);
  return processedData;
}

// Good: clean async/await in tests
await expect(awsPlugin.monitorStack('update', cfData, { frequency: 10 }))
  .to.eventually.be.rejectedWith(ServerlessError, 'An error occurred');
// additional logic follows naturally
```

When refactoring legacy promise-based code, complete the migration in dedicated commits or PRs before adding new functionality. This prevents the codebase from having inconsistent async patterns that are difficult to understand and debug.