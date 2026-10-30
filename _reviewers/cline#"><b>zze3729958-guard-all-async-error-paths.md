---
title: Guard all async error paths
description: Every promise chain, detached async operation, and event-emitting stream/process
  must have an explicit error handler so failures are reported instead of escaping
  as unhandled rejections or uncaught exceptions that can crash or hang the host process.
repository: cline/cline#"><b>zze3729958
label: Error Handling
language: TypeScript
comments_count: 7
repository_stars: 71067
---

Every promise chain, detached async operation, and event-emitting stream/process must have an explicit error handler so failures are reported instead of escaping as unhandled rejections or uncaught exceptions that can crash or hang the host process.

Concretely:
- When chaining `.then(onSuccess, onError)`, a throw inside `onSuccess` is not caught by `onError`. Use `.then(onSuccess).catch(onError)` instead so errors from both the original operation and the success handler are captured.
- Any method that can throw or reject (e.g. a process `kill()` call, a `write()` on a stream) must be wrapped and routed through the same failure path as other errors, not left for the caller to forget.
- Fire-and-forget ("detached") promises — e.g. `doSomething().then(...)` not awaited or returned — must always end in a `.catch()` (or equivalent) that at minimum logs the error; never leave a dangling promise with no rejection handler.
- Streams and child processes (e.g. `childProcess.stdin`) that can fail asynchronously after being handed off need an `error` listener attached before use, even if the failure will also be reported through another channel (e.g. `exit`/`close`), to prevent it from surfacing as an uncaught exception.
- When a callback passed to error-handling code (e.g. a logger or `onError` hook) might itself throw, wrap that call so it cannot escape and break the surrounding recovery logic.

Example:
```ts
// Bad: throw inside attach() is never caught
promise.then(
  (value) => attach(value), // may throw
  (error) => fail(error),
);

// Good: catches errors from both the original promise and attach()
promise.then((value) => attach(value)).catch((error) => fail(error));

// Bad: stdin error only surfaces as an uncaught exception
child.stdin.write(data);

// Good: always listen for stream errors
child.stdin.on("error", (error) => handleStdinFailure(error));
child.stdin.write(data);

// Bad: detached promise with no rejection handler
tracker.commit().then((hash) => updateMessage(hash));

// Good: detached work always has a terminal catch
tracker.commit().then((hash) => updateMessage(hash)).catch((error) => logger.error("commit failed", error));
```