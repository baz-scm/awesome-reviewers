---
title: Guard unattached async failures
description: Any promise or stream that is not directly awaited by its caller (detached
  `.then()` chains, fire-and-forget background work, Node stream/socket error emitters,
  `kill()`/`cancel()` calls on child processes or readers) must have an explicit error
  handler. Without one, the rejection or `error` event surfaces as an unhandled rejection
  or uncaught exception on...
repository: cline/cline?foo=bar
label: Error Handling
language: TypeScript
comments_count: 8
repository_stars: 71082
---

Any promise or stream that is not directly awaited by its caller (detached `.then()` chains, fire-and-forget background work, Node stream/socket error emitters, `kill()`/`cancel()` calls on child processes or readers) must have an explicit error handler. Without one, the rejection or `error` event surfaces as an unhandled rejection or uncaught exception on the host process, which can crash the whole process (extension host, CLI, daemon) rather than just failing the operation that triggered it.

Concretely:
- Chain `.then(onSuccess).catch(onFailure)` rather than `.then(onSuccess, onFailure)` when `onSuccess` itself can throw — the two-argument form only catches a rejected input promise, not an exception thrown inside the fulfillment handler.
- Attach `.catch()` to every promise you do not await, even when the operation is "best effort" (e.g., `reader.cancel()`, `kill()`, a background checkpoint commit). A caught error should at minimum be logged; it must never be allowed to propagate as an unhandled rejection.
- Add an `"error"` listener to any stream/socket (`stdin`, sockets, pipes) you write to or read from asynchronously. A process that exits or closes its pipe mid-write fails that write asynchronously on the stream, not on the process handle, so the write's caller never sees it unless a listener is attached.
- When parsing or acting on untrusted/external data inside an event handler (e.g., a socket `"message"` handler), wrap the work in `try/catch` and convert failures into a controlled recovery path (close the connection, reject pending work) instead of letting the handler throw synchronously out of the event loop.

Example of the two-argument pitfall:
```ts
// Bad: an exception thrown inside attach() escapes as an unhandled rejection.
promise.then(attach, onSpawnError);

// Good: covers failures from both the promise and the success handler.
promise.then(attach).catch(onSpawnError);
```

Example of a stream write failure:
```ts
// Bad: a write that fails after the child exits crashes the host process.
child.stdin.write(payload);

// Good: listen for the stream's own error and route it into recovery.
child.stdin.on("error", (error) => {
  // record/log, then fail pending work or close the connection
});
```

Treat "this is only a cleanup/best-effort call" as a reason to add a no-op `.catch()`, not a reason to skip error handling altogether.