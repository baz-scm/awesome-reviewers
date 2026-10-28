---
title: Guard and classify async errors
description: Every promise that isn't awaited by its caller — spawned child-process
  handles, fire-and-forget writes, background retries, detached `.then()` chains —
  must have an explicit error handler. A rejection with nothing attached becomes an
  unhandled rejection that can crash the host process (extension host, CLI, daemon),
  not just fail silently. Prefer...
repository: cline/cline#中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中
label: Error Handling
language: TypeScript
comments_count: 19
repository_stars: 70984
---

Every promise that isn't awaited by its caller — spawned child-process handles, fire-and-forget writes, background retries, detached `.then()` chains — must have an explicit error handler. A rejection with nothing attached becomes an unhandled rejection that can crash the host process (extension host, CLI, daemon), not just fail silently. Prefer `.then(onSuccess).catch(onError)` over `.then(onSuccess, onError)`, since the latter only covers the original promise and not synchronous throws inside `onSuccess`. When killing processes, closing streams, or detaching listeners, wrap or catch any call that can itself throw/reject so cleanup never escapes as an unhandled exception.

When catching errors, don't collapse distinct failure cases into one generic branch. Inspect what actually happened (timeout vs. provider error, missing-session vs. other RPC failure, aborted vs. genuine failure, "nothing to compact" vs. "retry failed") before deciding whether to retry, surface, or record success. A catch-all that defaults to "retryable" or "completed" can hide real failures (e.g. marking a sync tool call `completed` without checking `finishReason === "error"`, or granting a fresh retry budget to any timeout regardless of whether the SDK already retried). Likewise, don't let a later, broader error handler overwrite a more specific status that was already recorded (e.g. a provider error landing during shutdown must not turn a session's `cancelled` into `failed`; a context-overflow error's provider details must not be cleared just because the message text differs from `lastError`).

Preserve the original error's context (message, cause, status code, request id) as it propagates through wrapping and telemetry layers, and record failures at the point they happen rather than inferring them indirectly — so the error surfaced to users and recorded in telemetry always reflects the real, specific cause of failure.

```ts
// Bad: unattached rejection can crash the process, and failure type is not distinguished.
void spawnPromise.then(attach);

// Good: every branch of the chain is covered, and failure handling is explicit.
void spawnPromise.then(attach).catch((error) => handle.fail(toError(error)));
```