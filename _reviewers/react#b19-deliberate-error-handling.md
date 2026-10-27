---
title: Deliberate error handling
description: 'When catching exceptions, be intentional rather than swallowing indiscriminately.
  Only catch the specific error conditions you expect, and rethrow (or otherwise propagate)
  anything else so real bugs aren''t hidden:'
repository: facebook/react#b19
label: Error Handling
language: JavaScript
comments_count: 7
repository_stars: 251893
---

When catching exceptions, be intentional rather than swallowing indiscriminately. Only catch the specific error conditions you expect, and rethrow (or otherwise propagate) anything else so real bugs aren't hidden:

```js
try {
  unlinkSync(path);
} catch (err) {
  // Only ignore the expected case; rethrow everything else.
  if (err.code !== 'ENOENT') {
    throw err;
  }
}
```

When you do handle or report an error, preserve the original failure information instead of discarding it. Use `cause` or include the underlying error/message so the root cause is still discoverable:

```js
try {
  const hooksTree = inspectHooksOfFiberWithoutDefaultDispatcher(fiber, dispatcher);
} catch (error) {
  // Keep the original error as context instead of swallowing it.
  return {error: new Error('Failed to inspect hooks.', {cause: error})};
}
```

Never let a fallback path silently produce different behavior on failure — at minimum log/warn, and fail loudly (throw) if the fallback itself is unreliable, rather than continuing silently with a possibly-wrong result.

Avoid throwing conditionally based on environment flags (e.g. `__DEV__`); a thrown error should behave the same in dev and prod. If you want extra diagnostics only in dev, use `console.error` there instead of `throw`.

When invoking callbacks or user-supplied code (e.g. event handlers, dispatched callbacks, `onRecoverableError`-style hooks), isolate each call so a failure in one doesn't prevent others from running, and use `try/finally` around bookkeeping (like deleting a pending-callback map entry) so failures don't leak state:

```js
const callback = pendingCallbacks.get(requestId);
if (callback) {
  try {
    callback(response);
  } finally {
    pendingCallbacks.delete(requestId);
  }
}
```

Applying this consistently — narrow catches, preserved causes, no dev-only throws, and failure-isolated callbacks with proper cleanup — keeps error paths predictable and prevents masked bugs or resource leaks.