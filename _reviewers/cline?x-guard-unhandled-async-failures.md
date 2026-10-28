---
title: Guard unhandled async failures
description: Any asynchronous operation that is not directly awaited by its immediate
  caller — a detached `.then()` chain, an event-listener callback, a child-process/stream
  lifecycle call, or work started from inside another callback — must have an explicit
  error handler. Without one, a rejection or thrown exception escapes as an unhandled
  rejection or uncaught...
repository: cline/cline?x
label: Error Handling
language: TypeScript
comments_count: 6
repository_stars: 70983
---

Any asynchronous operation that is not directly awaited by its immediate caller — a detached `.then()` chain, an event-listener callback, a child-process/stream lifecycle call, or work started from inside another callback — must have an explicit error handler. Without one, a rejection or thrown exception escapes as an unhandled rejection or uncaught exception, which in many hosts (Node CLI, extension host, daemon) can terminate the whole process over a failure that was otherwise recoverable (a killed sandbox process, a hook closing its stdin early, a malformed WebSocket frame, a detached checkpoint commit).

Concrete patterns to watch for and fix:
- `promise.then(onSuccess, onError)` only catches a rejected `promise`, not an exception thrown inside `onSuccess`. Use `promise.then(onSuccess).catch(onError)` (or wrap in try/catch) so both paths are covered.
- A detached `.then(...)` with no trailing `.catch(...)` (e.g. `tracker.commit().then(async (hash) => {...})`) must end in `.catch(error => log(...))`, even if the original flow "silently failed" before.
- Methods like `kill()` that can throw synchronously or return a rejected promise must be wrapped by the caller (`try { child.kill() } catch (error) { fail(error) }`), especially when the result is otherwise ignored (`.finally(...)` without a preceding `.catch`).
- Streams and child processes need an `error` listener on every stream that can fail independently of the process `exit`/`close` event (e.g. `child.stdin.on("error", ...)`), so a failed write after the process died doesn't surface as a raw Node warning or crash.
- Parsing untrusted data (`JSON.parse` on socket payloads) inside an event listener must be wrapped in try/catch; treat a parse failure as a transport-level error (e.g. close the connection and let normal reconnect/retry logic take over) rather than letting it throw inside the listener.

Example of the safe pattern:
```ts
child.stdin.on("error", (error) => {
  // record/log, don't let it become an uncaught exception
  this.stdinFailure = toErrorMessage(error);
});

promise
  .then((value) => doWork(value))
  .catch((error) => this.fail(error));
```

When reviewing code that starts background work, kills a process, or listens on a stream, confirm every failure path ends in an explicit catch/handler rather than relying on the surrounding `try`/`catch` of unrelated code to cover it.