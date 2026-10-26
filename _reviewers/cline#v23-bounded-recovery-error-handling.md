---
title: Bounded Recovery Error Handling
description: 'When implementing failure handling and recovery, enforce four rules:
  (1) classify errors and apply only bounded, semantically-correct retries; (2) never
  lose the original failure—record best-effort diagnostics but rethrow the original
  error; (3) prevent unhandled async failures (detached promises, stream EPIPE, kill/reject
  paths); (4) keep retry...'
repository: cline/cline#v23
label: Error Handling
language: TypeScript
comments_count: 11
repository_stars: 70889
---

When implementing failure handling and recovery, enforce four rules: (1) classify errors and apply only bounded, semantically-correct retries; (2) never lose the original failure—record best-effort diagnostics but rethrow the original error; (3) prevent unhandled async failures (detached promises, stream EPIPE, kill/reject paths); (4) keep retry invariants—retries must not accidentally “flip” durable state/UI or drop already-completed side effects.

1) Classify before retrying
- Timeouts and “session lost” are not always transient. Only enable retry when the semantics say the operation can be safely replayed.
- Example pattern (MCP session lost / re-handshake):
```ts
async function withSessionRecovery<T>(op: (client: Client)=>Promise<T>): Promise<T> {
  const client = await ensureConnectedClient();
  try {
    return await op(client);
  } catch (err) {
    if (!isSessionLost(err)) throw err; // do not blanket-retry all errors
    const recovered = await recoverSession(client);
    return await op(recovered);
  }
}
```
- Example pattern (timeouts): don’t grant whole-turn retry just because the error is a timeout; treat it as “client stopped waiting” unless you can prove the provider request is safe to replay.

2) Record diagnostics best-effort, but preserve the original error
- If recovery/recording fails, it must not replace the underlying failure.
```ts
try {
  await primaryOperation();
} catch (primaryErr) {
  try { await recordFailure(primaryErr); } catch {/* log only */}
  throw primaryErr; // keep original failure semantics
}
```

3) Handle async failures that would otherwise escape
- Any detached promise must have a `.catch()` (or be awaited) so failures don’t become unhandled rejections.
```ts
// Bad: .then(async ...) without catch
somePromise.then(async () => { /* ... */ });

// Good
somePromise
  .then(async () => { /* ... */ })
  .catch((e) => console.error('checkpoint commit failed', e));
```
- For subprocess/stream integration: attach listeners for async write/read failures (e.g., stdin EPIPE) and ensure kill/restart failures are routed through the same controlled error/fail path rather than causing unhandled rejections.

4) Preserve invariants across retries
- Recovery must keep state consistent: restore “working” flags before/after rebuild; requeue failed persistence batches; and don’t change durable UI/runtime status when a retry is expected to keep the session running.
- If the system already executed side effects (e.g., provider tool calls), a retry must not replay them or must retain their results so history/output remains truthful.

Practical checklist for PRs
- For every catch/retry branch: what exact error class triggers it, and why is retry safe?
- Are all async callbacks/promises handled (no detached unhandled rejection)?
- Are stream/subprocess stdin/stdout/stderr errors absorbed or routed to the run outcome?
- Does failure recording ever mask/rewrite the original error?
- Do retries preserve invariants (UI status, durable state, and already-completed side effects)?