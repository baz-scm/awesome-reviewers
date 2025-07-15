---
title: Async error callbacks
description: When handling asynchronous operations, especially those that might continue
  running in the background after the main consumer has moved on, provide error callback
  options to ensure errors are properly reported and handled. This pattern prevents
  silent failures in background tasks and enables proper logging, monitoring, and
  recovery.
repository: vercel/ai
label: Error Handling
language: TypeScript
comments_count: 3
repository_stars: 15590
---

When handling asynchronous operations, especially those that might continue running in the background after the main consumer has moved on, provide error callback options to ensure errors are properly reported and handled. This pattern prevents silent failures in background tasks and enables proper logging, monitoring, and recovery.

For example, when consuming streams:

```typescript
// Without error handling - errors might be silently lost
result.consumeStream(); // no await

// With error handling - errors are properly reported
result.consumeStream(error => {
  console.log('Error during background stream consumption: ', error);
  // Optional: report to monitoring system
});
```

This approach is particularly important for background operations like stream consumption where the operation continues even when the client response is aborted (e.g., when a browser tab is closed). By implementing error callbacks, you ensure that errors are visible and actionable rather than silently failing.