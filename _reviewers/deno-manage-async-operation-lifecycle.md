---
title: Manage async operation lifecycle
description: When working with async operations, carefully manage execution context
  and resource references across await boundaries to prevent context corruption and
  resource leaks.
repository: denoland/deno
label: Concurrency
language: TypeScript
comments_count: 2
repository_stars: 103714
---

When working with async operations, carefully manage execution context and resource references across await boundaries to prevent context corruption and resource leaks.

For execution context, avoid patterns where context enters/exits span async boundaries, as context may not be properly restored after await points. Instead, structure code to contain async operations within the context scope:

```js
// Problematic - context lost across await
if (TRACING_ENABLED) {
  span = builtinTracer().startSpan(this.method, { kind: 2 });
  context = enterSpan(span);
  // await operations here lose context
}

// Better - use IIFE to contain async operations
const old = getAsyncContext();
try {
  setAsyncContext('inside operation');
  return (async () => {
    await asyncOperation();
    // context preserved here
  })();
} finally {
  setAsyncContext(old);
}
```

For resource management, distinguish between ongoing and future async operations when managing references. Use unref/ref patterns to handle current operations without affecting future ones:

```js
// Unref ongoing reads but not future reads
if (this.unref) {
  this.unref();  // Clear current operation references
  this.ref();    // Re-establish for future operations
}
```

This prevents resource leaks while maintaining proper reference counting for subsequent async operations.