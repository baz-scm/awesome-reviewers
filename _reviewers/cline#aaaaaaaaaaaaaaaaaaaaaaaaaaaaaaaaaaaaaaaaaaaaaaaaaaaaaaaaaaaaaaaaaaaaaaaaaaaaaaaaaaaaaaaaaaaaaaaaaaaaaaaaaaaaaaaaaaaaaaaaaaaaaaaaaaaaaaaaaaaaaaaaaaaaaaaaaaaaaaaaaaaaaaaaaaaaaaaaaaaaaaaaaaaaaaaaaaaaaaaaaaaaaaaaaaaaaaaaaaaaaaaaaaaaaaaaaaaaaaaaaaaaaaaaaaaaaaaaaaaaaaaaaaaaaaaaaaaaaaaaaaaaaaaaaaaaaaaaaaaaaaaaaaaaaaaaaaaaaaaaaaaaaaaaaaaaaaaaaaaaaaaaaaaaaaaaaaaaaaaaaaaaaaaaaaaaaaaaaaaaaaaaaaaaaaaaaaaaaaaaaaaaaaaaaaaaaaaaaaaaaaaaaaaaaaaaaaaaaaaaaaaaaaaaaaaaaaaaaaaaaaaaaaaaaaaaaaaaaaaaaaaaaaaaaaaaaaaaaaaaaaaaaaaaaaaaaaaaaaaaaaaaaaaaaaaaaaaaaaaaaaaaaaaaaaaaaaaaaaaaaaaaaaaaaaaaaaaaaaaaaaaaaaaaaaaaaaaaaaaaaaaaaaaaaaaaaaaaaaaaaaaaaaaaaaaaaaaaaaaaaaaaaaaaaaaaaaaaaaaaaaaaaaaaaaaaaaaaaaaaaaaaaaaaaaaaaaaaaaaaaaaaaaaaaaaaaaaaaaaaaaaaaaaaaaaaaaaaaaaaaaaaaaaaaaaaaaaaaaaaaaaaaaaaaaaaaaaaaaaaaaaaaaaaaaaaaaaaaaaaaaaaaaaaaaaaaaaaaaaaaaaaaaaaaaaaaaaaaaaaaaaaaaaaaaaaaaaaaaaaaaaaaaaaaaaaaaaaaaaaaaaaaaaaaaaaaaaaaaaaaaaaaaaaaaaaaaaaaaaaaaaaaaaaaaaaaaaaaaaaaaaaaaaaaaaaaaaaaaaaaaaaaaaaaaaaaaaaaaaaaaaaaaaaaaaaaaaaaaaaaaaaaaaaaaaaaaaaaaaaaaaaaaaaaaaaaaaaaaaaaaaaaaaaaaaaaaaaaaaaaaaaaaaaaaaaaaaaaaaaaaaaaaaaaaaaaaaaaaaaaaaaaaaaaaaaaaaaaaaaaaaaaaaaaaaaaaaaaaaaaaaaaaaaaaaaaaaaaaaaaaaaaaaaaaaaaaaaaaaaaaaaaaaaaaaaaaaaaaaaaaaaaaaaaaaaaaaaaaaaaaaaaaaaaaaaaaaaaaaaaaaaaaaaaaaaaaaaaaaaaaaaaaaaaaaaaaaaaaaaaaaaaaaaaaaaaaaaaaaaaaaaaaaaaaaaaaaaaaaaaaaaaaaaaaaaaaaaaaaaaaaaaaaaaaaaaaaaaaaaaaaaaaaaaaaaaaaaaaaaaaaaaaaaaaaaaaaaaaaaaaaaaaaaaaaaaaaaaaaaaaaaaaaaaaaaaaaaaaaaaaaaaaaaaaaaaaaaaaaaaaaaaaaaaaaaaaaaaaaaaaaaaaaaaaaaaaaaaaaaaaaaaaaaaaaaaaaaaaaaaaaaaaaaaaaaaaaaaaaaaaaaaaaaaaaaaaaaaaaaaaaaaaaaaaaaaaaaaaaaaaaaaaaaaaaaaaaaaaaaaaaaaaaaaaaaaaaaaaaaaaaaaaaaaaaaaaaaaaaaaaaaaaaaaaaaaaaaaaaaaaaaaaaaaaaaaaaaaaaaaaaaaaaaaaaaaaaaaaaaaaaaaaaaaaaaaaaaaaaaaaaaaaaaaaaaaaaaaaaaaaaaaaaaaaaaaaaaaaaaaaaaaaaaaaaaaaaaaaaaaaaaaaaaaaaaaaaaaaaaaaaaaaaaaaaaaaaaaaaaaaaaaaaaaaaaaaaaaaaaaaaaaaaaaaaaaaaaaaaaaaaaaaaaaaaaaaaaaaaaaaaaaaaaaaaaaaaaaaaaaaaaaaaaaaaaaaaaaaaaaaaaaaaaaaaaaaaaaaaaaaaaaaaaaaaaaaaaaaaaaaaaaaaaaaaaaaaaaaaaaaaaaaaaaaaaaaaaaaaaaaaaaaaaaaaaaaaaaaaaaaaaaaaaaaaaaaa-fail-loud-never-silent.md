---
title: Fail loud, never silent
description: 'Treat every failure path as a first-class thing to handle, not an afterthought:


  1. **Never leave a promise unguarded.** Any promise that isn''t awaited by its caller
  (fire-and-forget background work, event-emitter callbacks, stream `.then()` chains,
  a detached `child.stdin` write) must have an explicit rejection handler attached
  at the point it is created....'
repository: cline/cline#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
label: Error Handling
language: TypeScript
comments_count: 18
repository_stars: 70973
---

Treat every failure path as a first-class thing to handle, not an afterthought:

1. **Never leave a promise unguarded.** Any promise that isn't awaited by its caller (fire-and-forget background work, event-emitter callbacks, stream `.then()` chains, a detached `child.stdin` write) must have an explicit rejection handler attached at the point it is created. An uncaught rejection on a stream or background task becomes a process-crashing uncaught exception, not a recoverable error.
   ```ts
   // Bad: a failed cancel() or commit() becomes an unhandled rejection
   reader.cancel();
   this.checkpointTracker.commit().then(onSuccess);

   // Good
   reader.cancel().catch(() => {});
   this.checkpointTracker.commit().then(onSuccess, (error) =>
     logger.error("checkpoint commit failed", error),
   );
   ```

2. **Classify errors by actual cause before deciding how to react.** Don't collapse distinct failure modes (auth vs. not-found vs. timeout vs. missing-prerequisite vs. transient network) into one generic message or one fallback path. A blanket "check your credentials" message for every git failure, an unconditional archive-fallback that also fires for a missing Git binary, or a `TimeoutError` treated as automatically retryable all hide the real cause and can trigger the wrong recovery. Inspect the specific error (exit code, status code, error text) and branch accordingly; keep diagnostics (redacted) for anything you can't classify.

3. **Never let failure masquerade as success.** If an operation didn't actually succeed — a tool returned `success: false` without `isError`, a custom checkpoint hook returned nothing, a write failed but you still returned the old "it worked" shape — surface that as a real failure in the return value/state instead of defaulting to a happy path. Record it explicitly (e.g., a `skipReason`/`failed` status) so downstream logic and telemetry don't treat a failure as a win.

4. **Scope error/success state correctly and reset it at the real boundary.** State that describes "the outcome of this turn/request/session" must be reset at the start of that exact unit of work, before any fallible setup, so a later unit never inherits a stale success/error classification from a previous or unrelated one (e.g., clearing `lastFinishReason` only at the true top of a turn, not at some earlier point that still has fallible steps before it). Avoid re-deriving this classification logic in multiple places — reuse a single source of truth so the rules can't drift apart.

5. **On partial failure, restore a consistent state rather than leaving a hybrid one.** If an action fails partway through a mutation (rebuild, swap, scope change), roll back whatever was changed before rethrowing, and only commit "success" flags/state after the operation fully completes. A caller's catch block should not have to guess whether a side effect landed.

6. **Keep failure messages honest and minimal.** Don't log or display credentials, tokens, or raw hook/process output in error text; redact first. But do keep enough detail (command, exit code, phase) for the message to be diagnosable — a maximally generic message is as unhelpful as leaking secrets.