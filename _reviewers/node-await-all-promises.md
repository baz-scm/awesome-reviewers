---
title: Await all promises
description: Always explicitly await all asynchronous operations, especially in cleanup
  code paths and resource management. Failing to properly await promises can lead
  to race conditions, resource leaks, and unpredictable behavior in concurrent environments.
repository: nodejs/node
label: Concurrency
language: JavaScript
comments_count: 4
repository_stars: 112178
---

Always explicitly await all asynchronous operations, especially in cleanup code paths and resource management. Failing to properly await promises can lead to race conditions, resource leaks, and unpredictable behavior in concurrent environments.

When writing concurrent code:

1. Await all async operations, especially file operations and resource cleanup:
```javascript
// Bad: Resource may not be fully closed when code continues
if (options.autoClose) this.close();

// Good: Ensures the resource is fully closed before continuing
if (options.autoClose) await this.close();
```

2. Use modern Promise patterns for cleaner async code:
```javascript
// Better: Use Promise.withResolvers() for cleaner promise creation
const { promise, resolve, reject } = Promise.withResolvers();
fs.stat(filePath, { signal }, (err, stats) => {
  if (err) {
    return reject(err);
  }
  resolve(stats);
});
await assert.rejects(promise, { name: 'AbortError' });
```

3. Ensure async context is preserved across asynchronous boundaries:
```javascript
// Ensure AsyncLocalStorage context is preserved in callbacks
const als = new AsyncLocalStorage();
als.run(123, () => {
  navigator.locks.request('lock-name', async (lock) => {
    // Context should be maintained across the async boundary
    assert.strictEqual(als.getStore(), 123);
  });
});
```

By properly awaiting promises and managing async context, you'll write more reliable concurrent code with fewer race conditions and resource leaks.