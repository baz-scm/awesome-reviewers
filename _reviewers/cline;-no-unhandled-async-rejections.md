---
title: No unhandled async rejections
description: Every promise chain, event-listener callback, and asynchronous write
  must have an explicit error handler; a rejection or thrown exception that nobody
  catches becomes an unhandled rejection or uncaught exception and can take down the
  whole host process (CLI, extension host, daemon), not just the operation that failed.
repository: cline/cline;
label: Error Handling
language: TypeScript
comments_count: 7
repository_stars: 70964
---

Every promise chain, event-listener callback, and asynchronous write must have an explicit error handler; a rejection or thrown exception that nobody catches becomes an unhandled rejection or uncaught exception and can take down the whole host process (CLI, extension host, daemon), not just the operation that failed.

In practice this means:
- A `.then(onSuccess, onError)` pair only catches a rejection of the original promise; it does not catch a synchronous throw inside `onSuccess` itself. Use `.then(onSuccess).catch(onError)` so both paths are covered.
- Any "fire-and-forget" promise (a detached `.then(...)` with no return, a cleanup call like `kill()` or `reader.cancel()` that can reject) needs its own `.catch()`, even if that handler just logs and swallows the error. Don't assume a downstream `.finally()` or caller will absorb it.
- A child process's `stdin`/socket write can fail asynchronously after the process/peer is already gone (EPIPE, closed connection). Attach an `error` listener to the stream itself — the failure surfaces there, not on the child or the original call site — and route it into the same failure-reporting path used for a normal exit/close.
- Inside event-listener callbacks (socket `message`, stream `data`, etc.), wrap code that can throw (e.g. `JSON.parse` on untrusted/wire data) in try/catch, and convert the failure into a controlled outcome (close the connection, reject the pending operation with a real error) rather than letting it escape as an uncaught exception in the listener.

Example of the fix pattern:
```ts
// Before: throws inside attach() becomes an unhandled rejection
void spawn().then(attach, onSpawnError);

// After: both the rejection and a throw inside attach are caught
void spawn().then(attach).catch(onFailure);
```

```ts
// Before: a failed write after the peer disappears is uncaught
child.stdin.write(data);

// After: the stream reports the failure where it actually happens
child.stdin.on("error", (error) => recordInputFailure(error));
```

When reviewing, flag any detached promise, `.then()` without a trailing `.catch()`, or process/stream callback that assumes the happy path, and require it to end in an explicit handler.