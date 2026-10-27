---
title: Consistent Error Isolation
description: 'When calling into code that may throw (user callbacks, event handlers,
  instruction handlers, tooling probes), treat errors as first-class: don’t silence
  them, don’t let them break unrelated work, and don’t corrupt lifecycle state.'
repository: facebook/react#b14
label: Error Handling
language: JavaScript
comments_count: 11
repository_stars: 251893
---

When calling into code that may throw (user callbacks, event handlers, instruction handlers, tooling probes), treat errors as first-class: don’t silence them, don’t let them break unrelated work, and don’t corrupt lifecycle state.

Apply these rules:
- Isolate exceptions per callback: wrap each callback invocation in try/catch so one failure doesn’t prevent subsequent cleanup/flushing.
- Prefer structured error propagation over silent omission: tests should assert errors/reasons; tooling should return an Error (optionally with `cause`) rather than dropping details.
- Keep behavior consistent across environments: avoid “throw only in __DEV__”; handle errors the same way in DEV and prod (or log/return without throwing).
- Preserve abort/closed semantics: once a request/stream is aborted or a response is closed, do not allow later failures to overwrite the primary abort reason.
- Avoid callback/resource leaks: if you register callbacks, ensure they’re removed in a finally block even if the callback throws.

Example (per-callback isolation + no callback leaks):

```js
const callbacks = new Map();

function handleResponse(msg) {
  if (msg.source !== 'eval-response') return;
  const {requestId, response} = msg.payload;
  const cb = callbacks.get(requestId);
  if (!cb) return;

  callbacks.delete(requestId); // or do in finally
  try {
    cb(response);
  } finally {
    callbacks.delete(requestId);
  }
}

function flushEvents(events) {
  for (const event of events) {
    try {
      event();
    } catch (e) {
      // Report/record, but continue flushing remaining work.
      onRecoverableError(e);
    }
  }
}
```

Use this standard to prevent “one bad callback breaks everything”, “errors disappear”, and “later errors overwrite the real failure/abort reason.”