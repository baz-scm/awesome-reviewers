---
title: Prevent unhandled rejections/exceptions
description: Any promise that is not directly awaited by its caller — fire-and-forget
  calls, detached `.then()` chains, socket/stream event handlers, and callbacks invoked
  by Node or a third-party library — must have an explicit, non-throwing rejection/error
  handler. A single failure deep in one of these paths otherwise becomes an unhandled
  rejection or uncaught...
repository: cline/cline#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
label: Error Handling
language: TypeScript
comments_count: 9
repository_stars: 70965
---

Any promise that is not directly awaited by its caller — fire-and-forget calls, detached `.then()` chains, socket/stream event handlers, and callbacks invoked by Node or a third-party library — must have an explicit, non-throwing rejection/error handler. A single failure deep in one of these paths otherwise becomes an unhandled rejection or uncaught exception that can crash the whole host process (CLI, extension host, daemon), not just fail the one operation.

This pattern recurred across unrelated subsystems:
- `promise.then(onSuccess, onError)` only catches a rejection of `promise` itself; if `onSuccess` throws (e.g. stream/socket setup inside an `attach` callback), that throw is unhandled. Prefer `promise.then(onSuccess).catch(onError)` so both paths are covered.
- A detached `checkpointTracker.commit().then(async (hash) => {...})` dropped the `.catch()` the old awaited version had, turning a failed git commit into an unhandled rejection.
- A `kill()`/cleanup call that can itself throw or reject was left unguarded at the end of a `.finally()` chain or fire-and-forget call.
- Handlers Node invokes with no awaiting caller (`child.stdin.on("error", ...)`, a WebSocket `message` handler that calls `JSON.parse` on untrusted data) must catch locally and convert the failure into a controlled outcome (fail pending requests, close/reset the connection) instead of letting the exception propagate and kill the process.
- Third-party dependencies that install process-wide `uncaughtException`/`unhandledRejection` handlers (and call `process.exit`) must be scoped or neutralized to only what they themselves installed, so they don't terminate the host for an error its own handler already chose to survive.

Apply this standard by:
- Never leaving a promise chain with only a success branch; pair every `.then()` with a `.catch()` (not just a second `.then()` argument), and ensure the catch handler itself cannot throw.
- Wrapping any listener/callback invoked outside of an awaited call site so thrown errors are caught and turned into a local, recoverable failure rather than re-thrown.
- Auditing new dependencies for process-level error handler registration and isolating their side effects (e.g., snapshot-and-diff around import) rather than letting them own process lifecycle.
- Adding a regression test that simulates the failure (a throwing attach, a rejected kill, a malformed frame, a dependency's exception handler) and asserts the process survives and the operation fails cleanly instead of crashing.

```ts
// Bad: a throw inside attach() is never caught.
promise.then(attach, onSpawnError);

// Good: covers both the rejection and any throw while handling success.
promise.then(attach).catch(onSpawnError);
```