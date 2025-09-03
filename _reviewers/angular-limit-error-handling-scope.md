---
title: limit error handling scope
description: When implementing error handling, carefully limit the scope of try-catch
  blocks to prevent cascading failures and ensure error handlers themselves cannot
  cause additional errors. Wrap only the specific operations that may throw, not the
  error handling logic itself.
repository: angular/angular
label: Error Handling
language: TypeScript
comments_count: 3
repository_stars: 98611
---

When implementing error handling, carefully limit the scope of try-catch blocks to prevent cascading failures and ensure error handlers themselves cannot cause additional errors. Wrap only the specific operations that may throw, not the error handling logic itself.

The key principle is that error handlers should be resilient and not introduce new failure points. If an error handler throws, it can mask the original error and make debugging significantly more difficult.

**Example of proper scope limiting:**

```typescript
// ❌ Bad: try-catch wraps both injection and error handler execution
try {
  const errorHandler = injector.get(INTERNAL_APPLICATION_ERROR_HANDLER, null);
  errorHandler?.(error);
} catch (err) {
  // This catches errors from both injection AND error handler execution
}

// ✅ Good: try-catch only wraps the injection call
try {
  const errorHandler = injector.get(INTERNAL_APPLICATION_ERROR_HANDLER, null);
} catch (err) {
  // Handle injection failure
  return;
}
// Error handler executes outside try-catch - if it throws, we want to know
errorHandler?.(error);
```

**Additional considerations:**
- For non-critical operations (like logging or debugging), consider ignoring errors entirely rather than propagating them
- Use conditional checks before processing to avoid unnecessary allocations and operations
- When errors are expected due to baseline API support, document why they're being ignored

This approach ensures that error handling remains predictable and doesn't introduce additional failure modes that could compromise system stability.