---
title: Contain and attribute errors
description: 'Two failure modes keep showing up in error handling: (1) an async failure
  that never reaches a `catch`/error listener and escapes as an unhandled rejection
  or uncaught exception, which can crash the host process, and (2) an error that is
  caught but then loses, overwrites, or misclassifies its real cause, so recovery
  logic or the user-facing message responds...'
repository: cline/cline#中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中
label: Error Handling
language: TypeScript
comments_count: 15
repository_stars: 70986
---

Two failure modes keep showing up in error handling: (1) an async failure that never reaches a `catch`/error listener and escapes as an unhandled rejection or uncaught exception, which can crash the host process, and (2) an error that is caught but then loses, overwrites, or misclassifies its real cause, so recovery logic or the user-facing message responds to the wrong problem.

For (1): any operation that can fail outside the normal call/await chain — a detached `.then()`/fire-and-forget promise, a `kill()`/cleanup call, a child process's `stdin`/`stdout` stream, an `EventEmitter`'s `"error"` event, a socket message handler — needs an explicit handler before it ships. Prefer `.then(onSuccess).catch(onFailure)` over `.then(onSuccess, onFailure)` when the success handler itself can throw, and always attach `stream.on("error", ...)` for anything with Writable/Readable sides. Example:

```ts
// Bad: a rejection from onAttach becomes an unhandled rejection
spawn().then(onAttach, onSpawnError);

// Good: failures in either stage are caught
spawn().then(onAttach).catch(onFailure);

// Bad: an async write failure after the child exits raises on the stream
child.stdin.end(data);

// Good
child.stdin.on("error", (err) => logOrFail(err));
child.stdin.end(data);
```

For (2): don't let a generic catch block, a state reset, or a broad fallback collapse distinct failure causes into one bucket. Preserve the specific error (type, code, phase, request id) through catch/rethrow and telemetry so a `ContextWindowOverflowError` isn't treated the same as a plain mismatch, a missing-dependency error isn't silently retried with a different transport, and a stale "last error" field isn't reused for an unrelated turn/request. When a fallback or default path is only valid for one class of failure, check that class explicitly instead of applying the fallback to every error; when provider/config facts needed to classify an error are missing, treat that as "unknown" rather than silently assuming the negative case. Add regression tests that assert the specific error attributes (not just "an error occurred") survive to the point they're reported or acted on.