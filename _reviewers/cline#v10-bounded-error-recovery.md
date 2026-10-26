---
title: Bounded Error Recovery
description: 'When handling failures, make recovery *safe* (bounded + idempotent)
  and *observable* (no silent hangs/unhandled rejections). Concretely:


  1) Catch both sync throws and async rejections'
repository: cline/cline#v10
label: Error Handling
language: TypeScript
comments_count: 9
repository_stars: 70869
---

When handling failures, make recovery *safe* (bounded + idempotent) and *observable* (no silent hangs/unhandled rejections). Concretely:

1) Catch both sync throws and async rejections
- Avoid patterns like `.then(fn, onError)` when `fn` can throw synchronously during stream/pipe setup. Use `.then(fn).catch(onError)` so the synthetic process/failure path always closes.

2) Classify errors before retrying
- Don’t “widen” retry eligibility just because an error looks like a timeout. Keep provider/phase-specific rules (e.g., timeouts ≠ proof the provider didn’t act).

3) Recovery must be bounded and replay-once
- For session loss/reconnect flows, detect the specific failure mode and replay at most once.
- Don’t delete/settle abandoned work unless the control plane confirms; keep state for retriable/network errors.

4) Preserve completed side effects and partial results
- If retries/recovery could repeat side effects (tool executions, dispatched prompts), preserve already-completed activity or skip replay beyond the safe boundary.

5) Never let stream write errors escape uncaught
- If you write to stdin (or any stream) while the other side can close early, attach an `error` listener to capture/annotate the failure (EPIPE/closed-stdin) rather than letting it become an uncaught exception or disappear.

Minimal patterns:

```ts
// 1) sync-throw safe async chain
void loadMxc()
  .then((mxc) => mxc.spawn(/*...*/))
  .then((sandboxed) => handle.attach(sandboxed))
  .catch((error) => {
    handle.fail(new Error(`Sandboxing failed: ${String(error)}`));
  });

// 2) retry gating
if (isTimeoutReason(error)) {
  // decide using timeout-phase rules; do NOT automatically grant whole-turn retry
  return handleOperationError(error);
}

// 3) replay-once recovery
try {
  return await operation(client);
} catch (e) {
  if (!isSessionLost(e) || options.signal?.aborted) throw e;
  const reconnected = await recoverSession(client);
  return await operation(reconnected); // exactly once
}

// 5) stream error capture
childProcess.stdin?.on('error', (err) => {
  stdinFailure = String(err); // store for later error report
});
```

Adopting these rules prevents the common failure modes surfaced across the codebase: unhandled promise/stream errors, incorrect retry expansion (timeouts), broken idempotency boundaries (duplicate sends/tool side effects), and unsafe finalization during partially-confirmed failures.