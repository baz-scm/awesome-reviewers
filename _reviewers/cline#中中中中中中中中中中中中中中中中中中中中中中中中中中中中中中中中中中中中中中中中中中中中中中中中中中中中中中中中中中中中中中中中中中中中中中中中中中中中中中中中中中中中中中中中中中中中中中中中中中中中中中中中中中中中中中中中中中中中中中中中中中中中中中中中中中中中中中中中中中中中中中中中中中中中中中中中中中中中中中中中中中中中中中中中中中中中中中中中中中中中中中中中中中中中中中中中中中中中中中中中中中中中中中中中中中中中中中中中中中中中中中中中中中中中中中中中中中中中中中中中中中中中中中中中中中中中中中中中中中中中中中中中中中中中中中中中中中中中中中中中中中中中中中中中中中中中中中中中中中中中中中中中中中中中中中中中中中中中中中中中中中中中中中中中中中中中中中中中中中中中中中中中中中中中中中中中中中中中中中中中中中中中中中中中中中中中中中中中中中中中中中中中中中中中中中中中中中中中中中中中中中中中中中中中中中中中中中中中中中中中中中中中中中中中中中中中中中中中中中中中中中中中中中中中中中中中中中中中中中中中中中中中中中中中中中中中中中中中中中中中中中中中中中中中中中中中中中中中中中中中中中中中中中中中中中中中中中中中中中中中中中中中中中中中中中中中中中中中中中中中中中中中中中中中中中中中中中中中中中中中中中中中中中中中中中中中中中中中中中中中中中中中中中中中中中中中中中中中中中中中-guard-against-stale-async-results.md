---
title: Guard against stale async results
description: 'A large share of concurrency bugs here came from code that started an
  async operation, then — once it resolved — unconditionally applied its result to
  shared mutable state (a cache, a UI slot, a session map, a tracked file) even though
  a newer operation, cancellation, or state change had since made that result obsolete.
  Examples: a slow `task.list` seed...'
repository: cline/cline#中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中
label: Concurrency
language: TypeScript
comments_count: 18
repository_stars: 70984
---

A large share of concurrency bugs here came from code that started an async operation, then — once it resolved — unconditionally applied its result to shared mutable state (a cache, a UI slot, a session map, a tracked file) even though a newer operation, cancellation, or state change had since made that result obsolete. Examples: a slow `task.list` seed overwriting a newer one, a stale set of UI suggestions being re-served after a refresh, a reconnect landing on a session another start had already replaced, a status write from an aborted turn clobbering the write from teardown, two overlapping account/account-scope switches applying out of order.

Treat "this async result may no longer be relevant by the time it resolves" as the default assumption whenever a callback, promise, or retry can write back to shared state. Apply one (or more) of these techniques:

1. **Generation/epoch guard.** Capture a monotonically increasing counter (or object identity) before starting the async work. Before applying the result, check the counter/identity is still current; if not, discard the result (and clean up any resource it opened).
   ```ts
   const generation = ++this.startGeneration;
   const result = await doWork();
   if (generation !** this.startGeneration) return; // superseded; discard
   this.apply(result);
   ```
2. **Claim exclusivity before the first await.** When a result must be delivered exactly once (resolving a pending question, consuming a queued prompt), synchronously claim/clear the shared slot *before* doing any async work, so a concurrent caller routes through the normal fallback path instead of racing to consume the same slot.
3. **Serialize via promise chaining instead of ad hoc flags.** When operations on the same key/session/account must apply in request order, chain each new request onto the tail of the previous one (`this.tail = this.tail.then(() => run())`) rather than relying on a busy boolean, so a second call waits for the first and then re-decides against fresh state.
4. **Build the replacement before tearing down the original.** When replacing a live resource (a session runtime, a worker, a connection), construct and install the new one first, then release the old one guarded by "only if it still occupies the slot" — never remove the old resource before the new one is in place, which creates a window where concurrent callers see nothing.
5. **Re-check conditions immediately before irreversible side effects**, since time passed during the await (e.g., re-verify a session isn't mid-teardown right before writing its terminal status).

Always pair this with resource cleanup on the "stale" branch (close sockets/handles, dispose detected-late connections, release worker copies) so discarding a superseded result doesn't leak. Add a regression test that holds one operation mid-flight while a second, newer one completes, and asserts the newer one wins and the stale one is a safe no-op.