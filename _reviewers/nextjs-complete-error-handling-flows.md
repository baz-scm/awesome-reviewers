---
title: "Complete error handling flows"
description: "Implement robust error handling patterns that ensure both proper resource cleanup and error context preservation."
repository: "vercel/next.js"
label: "Error Handling"
language: "TypeScript"
comments_count: 2
repository_stars: 133000
---

Implement robust error handling patterns that ensure both proper resource cleanup and error context preservation.

**Resource cleanup:** Always clean up resources such as timeouts, connections, and file handles using `finally` blocks or promise `.finally()` handlers to prevent memory leaks:

```javascript
const timeoutId = setTimeout(() => {
  processLookupController.abort(`Operation timed out after ${timeoutMs}ms`);
}, timeoutMs);

try {
  // Main operation code
  return await someAsyncOperation();
} catch (error) {
  // Error handling
} finally {
  // Cleanup runs regardless of success or failure
  clearTimeout(timeoutId);
}
```

**Error context preservation:** When catching and rethrowing errors, preserve the original error context using the `cause` property instead of modifying error messages directly:

```javascript
try {
  await instrumentationModule.register();
} catch (err) {
  // Preserve the original error while adding context
  throw new Error("An error occurred while loading instrumentation hook", { cause: err });
}
```

This approach maintains the original stack trace and error details while allowing you to add meaningful context for debugging.