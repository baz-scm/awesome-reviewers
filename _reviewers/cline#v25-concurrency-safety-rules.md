---
title: Concurrency Safety Rules
description: 'When async code crosses ownership boundaries (teardown, UI actions,
  replies, persistence, retries), prevent races by enforcing these rules.


  1) Claim ownership before any await'
repository: cline/cline#v25
label: Concurrency
language: TypeScript
comments_count: 13
repository_stars: 70891
---

When async code crosses ownership boundaries (teardown, UI actions, replies, persistence, retries), prevent races by enforcing these rules.

1) Claim ownership before any await
- If a callback resolves a “pending” action, claim it synchronously so no second submission can “win” during attachment/network awaits.

```ts
async function resolvePendingAsk(prompt?: string, deliverAttachments?: () => Promise<void>) {
  const resolve = pendingAskResolve;
  if (!resolve) return false;
  pendingAskResolve = undefined; // claim NOW

  const hasAttachments = !!deliverAttachments;
  if (hasAttachments) {
    await deliverAttachments!(); // safe: no one else can resolve the same ask
  }

  resolve(prompt ?? "");
  return true;
}
```

2) Await critical side-effects that must precede completion/dispose
- If the caller/teardown can dispose resources, you must await the async phase that writes durable/observable state (e.g., rule serving, debug-log entries, offer delivery) before returning.

3) Reject stale callbacks with per-update tokens
- Use revisions/generations/epochs to ensure late events can’t mutate current state.
- Every publish/update should bump a token; handlers must validate token equality before acting.

4) Make persistence/cleanup atomic or serialized
- For state writes that can overlap (shutdown vs running, overlapping retries, concurrent file pruning), serialize writes (promise chaining/queue) or use atomic “remove-if-unchanged” patterns (rename + compare-at-delete) rather than “check then unlink later”.

5) Make cancellation and timeouts end the whole wait
- Thread AbortSignal into sleeps, retries, and stream pumps.
- Avoid indefinite waits when the owner/client disconnects; fail fast with a user-appropriate error.
- On “settle”, clean up listeners/pipes to avoid background children keeping the host alive.

Applying these consistently prevents: out-of-order effects, stale UI actions, lost updates, overwritten shutdown status, orphaned retries/streams, and leaked subprocess resources.