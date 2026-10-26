---
title: Safe Error Propagation
description: 'Make error handling non-optional: every async boundary must catch both
  (1) promise rejections and (2) synchronous throws, and failures must be routed through
  a single explicit failure/cleanup path. Only retry when the error classification
  proves it’s safe; otherwise preserve the original failure (and any already-recorded/finished
  attribution) without...'
repository: cline/cline#v17
label: Error Handling
language: TypeScript
comments_count: 15
repository_stars: 70883
---

Make error handling non-optional: every async boundary must catch both (1) promise rejections and (2) synchronous throws, and failures must be routed through a single explicit failure/cleanup path. Only retry when the error classification proves it’s safe; otherwise preserve the original failure (and any already-recorded/finished attribution) without dropping output.

Actionable rules
1) Catch sync throws inside async setup
- If you do `promise.then(fn, onErr)`, it will not catch exceptions thrown *inside* `fn`.
- Prefer:

```ts
void someAsyncOperation()
  .then(() => attach())
  .catch((error) => fail(error));
```

2) Never ignore stream/socket stdin/write failures
- When writing to a child/server stream, register an `error` listener on the stream that receives the failure (EPIPE/EOF on Windows can surface there).
- Route it into the same “fail pending requests + close/terminate” path you use for normal exit/error.

```ts
child.stdin?.on('error', (err) => {
  recordStdinFailure(err);
  failPendingRequests(new Error('stdin write failed'));
});
```

3) Kill/timeouts must not produce unhandled rejections
- If `kill()`/cleanup can throw/reject, wrap it and route through `fail(...)` (or swallow deliberately), never let it become an unhandled rejection.

4) Classify errors before retrying
- Define what is transient vs permanent (e.g., timeout vs invalid-response vs unreachable).
- Gate retries on that classification; do not blanket-mark timeouts/rejections as retryable.
- If you’re already doing a bounded retry policy elsewhere, don’t bypass it from a secondary recovery path.

5) Preserve state attribution and don’t drop terminal/empty outcomes
- When a recovery/compaction/retry path runs, ensure it never silently converts “empty/errored/aborted” into success.
- If you already recorded a timeout reason/finish reason, preserve it through abort/retry paths rather than re-deriving from a string message.

6) “Best-effort bookkeeping” must never change the primary failure
- For checkpoint/persistence-style metadata writes: record failure info, but don’t mask the original error; report metadata errors separately.

Implementation checklist
- For every `attach`, `spawn`, `pipe`, or “start worker/process” code path: confirm there’s a single failure funnel that (a) rejects the right pending promise(s), (b) closes streams, and (c) terminates/cleans resources.
- For every retry: ensure the retry condition is derived from an explicit error classification and that recovery won’t replay unsafe side effects or drop required terminal output.