---
title: Propagate and clarify errors
description: 'When handling exceptions, only catch the specific error types your code
  is designed to handle, and always rethrow or otherwise propagate unexpected errors
  instead of swallowing them. Avoid pointless try/catch blocks that just rethrow the
  same error (`no-useless-catch`); prefer `try { return await promise } finally {
  ... }` when you only need cleanup logic:'
repository: HONOJS/HONO
label: Error Handling
language: TypeScript
comments_count: 5
repository_stars: 32741
---

When handling exceptions, only catch the specific error types your code is designed to handle, and always rethrow or otherwise propagate unexpected errors instead of swallowing them. Avoid pointless try/catch blocks that just rethrow the same error (`no-useless-catch`); prefer `try { return await promise } finally { ... }` when you only need cleanup logic:

```ts
// Avoid:
try {
  result = await callable
  return result
} catch (e) {
  throw e
} finally {
  endTime(c, name, precision)
}

// Prefer:
try {
  return await callable
} finally {
  endTime(c, name, precision)
}
```

When you do catch an exception, check its type explicitly (e.g. `if (error instanceof HTTPException)`) and rethrow anything you don't recognize, rather than silently absorbing it. If a caller can supply an optional error handler (e.g. `onError`) but doesn't, don't let the error disappear—log it (e.g. `console.error`) so failures remain visible.

Error messages should be clear, consistent, and informative: start with a capital letter, extract reusable messages into named constants (as done for `ERROR_MESSAGE_JSON` in body-limit middleware), and include both the actual and expected values to aid debugging, e.g.:

```ts
throw new Error(`unexpected key type: CryptoKey.type is ${key.type}, expected 'private' or 'secret'`)
```

Following these practices ensures failures are neither hidden nor misreported, and makes debugging and failure recovery predictable across the codebase.