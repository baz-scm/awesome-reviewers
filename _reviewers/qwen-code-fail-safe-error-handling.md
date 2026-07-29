---
title: Fail-safe Error Handling
description: 'Use fail-safe error handling everywhere in long-running / retrying flows:
  cleanup must be guaranteed, state/cursors must follow the intended retry semantics,
  and errors must remain diagnosable.'
repository: QwenLM/qwen-code
label: Error Handling
language: TypeScript
comments_count: 24
repository_stars: 26407
---

Use fail-safe error handling everywhere in long-running / retrying flows: cleanup must be guaranteed, state/cursors must follow the intended retry semantics, and errors must remain diagnosable.

Apply these rules:
1) Cleanup in finally, not best-effort.
- For every resource lifecycle (server, sockets, file handles, event subscriptions), ensure close/dispose happens in a try/finally even when other operations throw.

2) Decide per error kind: retry, terminal-skip, or bubble.
- If failure is retryable: do not advance cursors or dedup keys; rethrow so the poll loop retries.
- If failure is terminal (e.g., 404/410 deleted/transfer): skip only that item and advance so you don’t wedge the batch.
- If you can’t guarantee either, at least record enough telemetry and avoid infinite loops.

3) Never “silently succeed” after a failed dispatch.
- If a delivery/dispatch fails, ensure the lane/process doesn’t mark the notification/comment as handled in a way that prevents retries, or it will permanently lose messages.
- Conversely, if you want at-most-once semantics, record only on successful dispatch.

4) Preserve diagnostics.
- When wrapping errors, preserve the cause: `throw new X(message, { cause: error })`.
- Use structured/typed errors (e.g., EXECUTION_DENIED vs UNHANDLED_EXCEPTION) so telemetry and fallback logic behave correctly.

5) Classify timeouts/cancellations/quotas correctly.
- Treat “quota exhausted” as fast-fail without re-triggering generic rate-limit retry loops.
- Treat user cancellation distinctly from “unavailable picker”/display errors.

Example pattern (cursor + fail-safe dispatch):

```ts
async function processBatch(items: Item[], cursor: Cursor) {
  let firstError: unknown;
  for (const item of items) {
    try {
      const ok = await dispatch(item);
      if (ok) cursor.markHandled(item.id);
      // advance cursor for success (or terminal skip)
    } catch (err) {
      if (isTerminal(err)) {
        // skip permanently but advance cursor so you don’t wedge
        cursor.markHandled(item.id);
        continue;
      }
      // retryable: do NOT advance cursor/dedup keys
      firstError ??= err;
    }
  }
  if (firstError) throw firstError;
  cursor.advanceToLatest();
  await cursor.save();
}

function isTerminal(err: unknown): boolean {
  // 404/410 patterns; also treat auth/permission without retry-after as terminal
  return err instanceof HttpError && (err.status === 404 || err.status === 410);
}
```

This standard prevents the common failure modes seen across the discussions: orphaned state from missing cleanup, lost messages from swallowing/“marking handled” on failed dispatch, infinite poll livelocks from not advancing cursor, and operator-blind failures from lost error context.