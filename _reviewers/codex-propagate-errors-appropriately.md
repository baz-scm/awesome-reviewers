---
title: Propagate errors appropriately
description: Allow errors to bubble up to their appropriate handling layers rather
  than catching them prematurely. Catching errors at incorrect levels can prevent
  proper error handling, recovery mechanisms, and specialized handlers (like rate
  limiting logic) from functioning as intended.
repository: openai/codex
label: Error Handling
language: TypeScript
comments_count: 3
repository_stars: 31275
---

Allow errors to bubble up to their appropriate handling layers rather than catching them prematurely. Catching errors at incorrect levels can prevent proper error handling, recovery mechanisms, and specialized handlers (like rate limiting logic) from functioning as intended.

When designing error handling, consider:

1. Only catch errors at the level where you can meaningfully handle them
2. Let specialized error handling logic (like retry mechanisms) exist in a single place
3. Use appropriate error type checking when you do need to handle specific errors

```typescript
// Poor practice - catching errors too early without proper handling
try {
  await performOperation();
} catch (error) {
  console.error('Operation failed:', error);
  // No meaningful recovery or proper error propagation
}

// Better practice - let errors propagate to appropriate handlers
// In component code:
await performOperation(); // No try/catch here

// In higher-level error handling layer:
try {
  await executeComponentCode();
} catch (error) {
  if (error instanceof RateLimitError) {
    return await retryWithBackoff();
  } else if (error instanceof NetworkError) {
    // Specialized handling for network issues
  } else {
    // Log and propagate further if needed
    logger.error('Unhandled error:', error);
    throw error;
  }
}
```

This approach creates a cleaner separation of concerns, centralizes error handling logic, and ensures errors are handled at the most appropriate level.