---
title: defer async callbacks
description: Always ensure callbacks and event emissions are executed asynchronously
  to maintain proper timing and Node.js compatibility. Even when operations appear
  to complete synchronously, callbacks should be deferred using `queueMicrotask()`
  or `process.nextTick()` to match expected async behavior.
repository: cloudflare/workerd
label: Concurrency
language: TypeScript
comments_count: 3
repository_stars: 6989
---

Always ensure callbacks and event emissions are executed asynchronously to maintain proper timing and Node.js compatibility. Even when operations appear to complete synchronously, callbacks should be deferred using `queueMicrotask()` or `process.nextTick()` to match expected async behavior.

This is critical for maintaining consistent execution order and preventing timing-related bugs. Synchronous callback execution can break assumptions about when code runs relative to other async operations.

Example of proper async callback deferral:
```javascript
// Instead of calling callback immediately
callback?.();

// Defer the callback execution
queueMicrotask(() => callback?.());
```

The key principle is that callbacks should execute after the current execution context completes, allowing other queued operations to run in the expected order. This ensures compatibility with Node.js behavior where callbacks are typically asynchronous even for operations that complete immediately.