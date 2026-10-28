---
title: Handle async failures explicitly
description: Every promise, stream, child process, and event emitter must have its
  failure path handled explicitly — never leave a detached `.then()`, a fire-and-forget
  async call, a stdin/socket `error` listener, or a `kill()`/cleanup call without
  a `.catch()` or try/catch. An unhandled rejection or exception from one of these
  (e.g. `promise.then(onSuccess)` with no...
repository: "cline/cline\t"
label: Error Handling
language: TypeScript
comments_count: 17
repository_stars: 70947
---

Every promise, stream, child process, and event emitter must have its failure path handled explicitly — never leave a detached `.then()`, a fire-and-forget async call, a stdin/socket `error` listener, or a `kill()`/cleanup call without a `.catch()` or try/catch. An unhandled rejection or exception from one of these (e.g. `promise.then(onSuccess)` with no error branch, a stream that fails mid-write, a process-tree kill that throws) surfaces as an uncaught exception that can crash the whole host process, not just fail the operation.

```ts
// Bad: exception inside attach(), or a rejected kill(), escapes as an unhandled rejection
void loadMxc().then(
  (mxc) => handle.attach(mxc), // throws here are never caught
);
sandboxed.kill(); // may throw synchronously or reject

// Good: every failure path is funneled to a single handler
void loadMxc().then(
  (mxc) => handle.attach(mxc),
  (error) => handle.fail(toError(error)),
).catch((error) => handle.fail(toError(error)));
```

When writing the catch/error-handling logic itself, avoid broad, undifferentiated handling that masks the real cause or applies the wrong recovery:
- Don't classify by a loose signal (a regex on an error message, "any non-2xx response", "any thrown error") when a narrower, verifiable condition is available (a specific exit code plus its stderr text, a specific HTTP status, an explicit error type). A catch-all can silently treat an unrelated failure (auth error, size-limit error, server restart) as the one case you meant to handle, producing a wrong fallback or a misleading message.
- Never let a generic recovery path (archive fallback, retry, default branch, "not found") replace a specific, actionable error (missing dependency, auth failure, size limit) — surface the real cause when the condition isn't the one the fallback was built for.
- Preserve the original error/diagnostic details through retries and rewrapping; don't reset or overwrite captured error state (`lastError`, provider details, finish reason) until you are certain the new value actually corresponds to the failure being reported, and reset such per-attempt/per-turn state at the start of the attempt rather than opportunistically midway through, so an earlier failure's cause is never attributed to a later one.
- Recording telemetry about a failure (best-effort logging, a `recordFailure` call) must never replace or suppress the original error; log and rethrow.

Add regression tests that reproduce the specific failure mode (a rejected kill, a parse error on a socket frame, a specific exit code) to lock in the fix.