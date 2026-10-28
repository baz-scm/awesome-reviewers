---
title: Guard every async failure
description: Every promise that isn't awaited by its caller (fire-and-forget writes,
  detached `.then()` chains, cleanup calls like `kill()` or `cancel()`) must have
  an explicit rejection handler, and that handler must itself be safe to throw from.
  `.then(onSuccess, onError)` only catches a rejected source promise — it does not
  catch an exception thrown inside...
repository: cline/cline#;sleep 4;
label: Error Handling
language: TypeScript
comments_count: 9
repository_stars: 70976
---

Every promise that isn't awaited by its caller (fire-and-forget writes, detached `.then()` chains, cleanup calls like `kill()` or `cancel()`) must have an explicit rejection handler, and that handler must itself be safe to throw from. `.then(onSuccess, onError)` only catches a rejected source promise — it does not catch an exception thrown inside `onSuccess` — so prefer `.then(onSuccess).catch(onError)` when `onSuccess` can fail. A stray rejection or exception here becomes an unhandled rejection/uncaught exception that can crash or hang the host process, independent of whatever error-reporting path the rest of the code already has.

Equally important: don't assume success just because a call resolved, exited 0, or lacks an explicit `isError`/`error` flag. Tool results can report `success: false` in their payload without setting `isError`; a process exit code can mean several different things depending on stderr; a sync code path can drop the same `finishReason === "error"` check an async path already applies. Check the actual result shape for failure, not just whether the promise settled, and keep that check consistent across every code path that produces the same kind of result (sync/async, recorded/replayed) so failures are never silently reported as success.

```ts
// Bad: throws inside attach() become unhandled rejections,
// and a non-zero kill() exit is never caught.
spawn().then(attach, onSpawnError);
process.kill(); // may throw

// Good: every stage that can throw is guarded.
spawn()
  .then(attach)
  .catch((error) => handle.fail(toError(error)));

try {
  process.kill();
} catch (error) {
  handle.fail(toError(error));
}
```

Apply the same discipline when a later catch block adds retry or recovery logic: don't overwrite the original failure with a stale captured value, and don't let a best-effort side write (telemetry, metadata) replace or suppress the real error — record it, then rethrow the original.