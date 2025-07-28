---
title: Extract complex inline logic
description: When functions contain complex inline logic or duplicated code, extract
  this logic into separate functions or shared utilities to improve readability and
  maintainability. Complex inline code makes functions harder to understand and test,
  while duplication creates synchronization issues and increases the likelihood of
  bugs.
repository: denoland/deno
label: Code Style
language: TypeScript
comments_count: 2
repository_stars: 103714
---

When functions contain complex inline logic or duplicated code, extract this logic into separate functions or shared utilities to improve readability and maintainability. Complex inline code makes functions harder to understand and test, while duplication creates synchronization issues and increases the likelihood of bugs.

For complex inline logic, create dedicated functions:
```typescript
// Instead of complex inline logic:
function mapToCallback(context, callback, onError) {
  return async function (req) {
    const asyncContext = getAsyncContext();
    setAsyncContext(context.asyncContext);
    try {
      // ... complex logic here ...
    } finally {
      // ... cleanup logic ...
    }
  };
}

// Extract into a separate function:
function mapToCallback(context, callback, onError) {
  return async function (req) {
    return handleRequestWithContext(req, context, callback, onError);
  };
}
```

For duplicated code between similar implementations (like sync/async versions), consider:
- Factoring out common functionality into shared utilities
- Using abstract base classes that handle the common logic
- Separating implementations into different files for easier maintenance

This approach reduces cognitive load, makes code easier to test, and prevents bugs that arise from maintaining multiple copies of similar logic.