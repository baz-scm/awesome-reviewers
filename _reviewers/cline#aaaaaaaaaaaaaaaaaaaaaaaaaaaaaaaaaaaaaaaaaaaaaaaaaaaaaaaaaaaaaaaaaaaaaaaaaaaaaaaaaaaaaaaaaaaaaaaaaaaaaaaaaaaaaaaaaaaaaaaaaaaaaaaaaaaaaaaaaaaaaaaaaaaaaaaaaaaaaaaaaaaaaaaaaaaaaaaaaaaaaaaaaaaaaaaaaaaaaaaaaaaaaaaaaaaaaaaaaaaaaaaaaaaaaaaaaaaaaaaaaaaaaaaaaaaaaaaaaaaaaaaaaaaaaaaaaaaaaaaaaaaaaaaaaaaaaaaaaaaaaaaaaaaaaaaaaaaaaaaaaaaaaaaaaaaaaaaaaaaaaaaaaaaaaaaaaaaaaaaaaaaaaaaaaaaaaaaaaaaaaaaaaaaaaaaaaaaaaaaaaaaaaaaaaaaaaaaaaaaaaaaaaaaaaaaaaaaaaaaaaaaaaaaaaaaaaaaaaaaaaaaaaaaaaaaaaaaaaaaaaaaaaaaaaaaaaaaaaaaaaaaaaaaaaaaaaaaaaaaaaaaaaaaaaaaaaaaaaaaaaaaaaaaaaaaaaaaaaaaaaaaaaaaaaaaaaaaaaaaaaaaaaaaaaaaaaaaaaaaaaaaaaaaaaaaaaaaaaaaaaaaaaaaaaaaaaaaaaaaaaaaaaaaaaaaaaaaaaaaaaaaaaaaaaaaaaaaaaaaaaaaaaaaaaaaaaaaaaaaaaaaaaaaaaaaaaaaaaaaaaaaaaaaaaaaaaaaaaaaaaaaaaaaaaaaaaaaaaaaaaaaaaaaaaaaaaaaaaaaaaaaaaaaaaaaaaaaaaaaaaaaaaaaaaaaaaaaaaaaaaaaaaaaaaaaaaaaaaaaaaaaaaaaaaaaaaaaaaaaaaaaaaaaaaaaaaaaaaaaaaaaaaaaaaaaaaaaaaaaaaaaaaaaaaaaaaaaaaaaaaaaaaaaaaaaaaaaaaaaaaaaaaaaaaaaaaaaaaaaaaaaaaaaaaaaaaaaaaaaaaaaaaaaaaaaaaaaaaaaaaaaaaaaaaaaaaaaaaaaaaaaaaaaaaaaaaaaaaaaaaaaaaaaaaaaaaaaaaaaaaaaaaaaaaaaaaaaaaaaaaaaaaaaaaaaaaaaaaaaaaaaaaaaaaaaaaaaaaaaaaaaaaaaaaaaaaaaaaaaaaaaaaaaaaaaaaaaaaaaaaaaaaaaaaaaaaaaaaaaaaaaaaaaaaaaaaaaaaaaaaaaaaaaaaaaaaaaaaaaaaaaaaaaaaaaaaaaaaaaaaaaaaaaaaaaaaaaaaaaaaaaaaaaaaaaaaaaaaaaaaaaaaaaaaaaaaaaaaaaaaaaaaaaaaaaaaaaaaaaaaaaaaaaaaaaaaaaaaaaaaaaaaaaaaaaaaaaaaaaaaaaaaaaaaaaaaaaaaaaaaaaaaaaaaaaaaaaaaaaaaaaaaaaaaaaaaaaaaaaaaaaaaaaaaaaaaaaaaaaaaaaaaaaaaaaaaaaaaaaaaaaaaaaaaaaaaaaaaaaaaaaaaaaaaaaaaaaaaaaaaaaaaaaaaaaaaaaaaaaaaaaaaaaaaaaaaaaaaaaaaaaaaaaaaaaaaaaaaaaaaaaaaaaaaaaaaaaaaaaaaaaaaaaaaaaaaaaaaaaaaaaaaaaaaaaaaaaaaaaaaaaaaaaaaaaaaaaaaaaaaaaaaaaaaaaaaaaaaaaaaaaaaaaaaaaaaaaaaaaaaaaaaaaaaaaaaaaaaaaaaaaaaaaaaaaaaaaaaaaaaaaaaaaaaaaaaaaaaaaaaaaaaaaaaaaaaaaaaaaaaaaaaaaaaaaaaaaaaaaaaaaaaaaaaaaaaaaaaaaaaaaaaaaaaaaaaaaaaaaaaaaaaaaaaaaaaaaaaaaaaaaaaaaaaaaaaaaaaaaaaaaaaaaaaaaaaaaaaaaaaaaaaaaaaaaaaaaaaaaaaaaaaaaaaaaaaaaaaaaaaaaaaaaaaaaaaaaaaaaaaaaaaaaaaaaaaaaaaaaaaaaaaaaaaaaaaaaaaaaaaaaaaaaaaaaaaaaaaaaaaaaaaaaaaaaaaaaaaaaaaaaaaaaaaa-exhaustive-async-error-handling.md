---
title: Exhaustive async error handling
description: 'Treat every failure path of an asynchronous operation as part of the
  contract, not an afterthought. Concretely:


  1. **Never leave a promise without a landing spot for rejection**, especially on
  fire-and-forget or detached calls: a `.then(onSuccess)` with no `.catch`, a synchronous
  throw inside a `.then` handler, a child-process `kill()`/stream `cancel()`...'
repository: cline/cline#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
label: Error Handling
language: TypeScript
comments_count: 20
repository_stars: 70970
---

Treat every failure path of an asynchronous operation as part of the contract, not an afterthought. Concretely:

1. **Never leave a promise without a landing spot for rejection**, especially on fire-and-forget or detached calls: a `.then(onSuccess)` with no `.catch`, a synchronous throw inside a `.then` handler, a child-process `kill()`/stream `cancel()` that can reject, or a socket/stdin error event with no listener. On most runtimes this becomes an unhandled rejection or uncaught exception that can terminate the whole host process, not just fail the one operation:
   ```ts
   // Bad: a throw inside attach(), or a rejected kill(), has nowhere to go.
   promise.then(attach, onSpawnError);

   // Good: every branch is caught and routed to the same failure handler.
   promise.then(attach, onSpawnError).catch(onSpawnError);
   kill(): void {
       try {
           this.process?.kill();
       } catch (error) {
           this.fail(error instanceof Error ? error : new Error(String(error)));
       }
   }
   ```

2. **Leave the system retryable after a failure, not permanently wedged.** If a flag, cache entry, or "live" marker is set optimistically before an operation and that operation fails, reset it (or roll it back) in the catch block so the next call/turn/session retries cleanly instead of repeating the same broken state forever (e.g. clearing a "connection is live" flag when a send reports the session missing, restoring a provider-activation flag only after the activation actually succeeds, clearing a pending-start record only once the deletion is actually confirmed).

3. **Preserve the original failure's diagnostic detail as it is wrapped or classified.** Don't let a generic `error_type` or a coarse status code replace fields (`error_status`, `error_code`, `requestId`, exit codes, HTTP status) that a provider/subsystem already reported — losing them blinds telemetry and makes incidents harder to triage.

4. **Don't let one catch-all handle causes that need different remedies.** A missing dependency, an auth failure, and a network blip are not the same problem; collapsing them into one fallback (e.g. silently switching transport, or granting a stale retry budget) can mask a configuration issue behind a transient-looking failure. Classify precisely enough to choose the narrowest correct recovery, and when in doubt, fail with an actionable, specific message rather than guessing.

Apply this checklist whenever you add a `.then`/`.catch`, a background retry, a fallback path, or new error metadata: confirm every rejection is handled, every optimistic state change has a rollback, every wrapped error keeps its useful fields, and every fallback is scoped to the failure it's actually meant to fix.