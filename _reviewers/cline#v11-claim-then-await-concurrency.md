---
title: Claim-Then-Await Concurrency
description: 'When coordinating async work, prevent invariants from being broken by
  overlapping “late completions”. Apply these rules:


  1) Claim ownership synchronously, before any await'
repository: cline/cline#v11
label: Concurrency
language: TypeScript
comments_count: 8
repository_stars: 70871
---

When coordinating async work, prevent invariants from being broken by overlapping “late completions”. Apply these rules:

1) Claim ownership synchronously, before any await
- If multiple submissions/requests can overlap, make the first one “own” the action immediately (e.g., set the pending resolver to undefined) before you await attachment delivery or network calls.

2) Never “late re-discover” the target of a background update
- If you schedule work to complete later, capture the exact object/message/id you will update at the time you enqueue the work, or serialize the operations. Don’t re-search global state later (it can point to the newest unrelated item).

3) Serialize writes or isolate per-operation state
- For shared status/buffers, either (a) chain updates per entity (per session/run/message), or (b) snapshot per operation so stragglers write into their own captured buffer.

4) Make cancellation/timeouts and cleanup part of settlement
- If you settle early (due to timeout/abort), ensure later events can’t keep resources alive (cancel timers, drop inherited pipes/listeners, disconnect late connections) and ensure no indefinite waits.

Code sketch (claim-before-await)
```ts
async function resolvePendingAsk({ prompt, deliverAttachments }: {
  prompt?: string;
  deliverAttachments?: (isCurrent: () => boolean) => Promise<void>;
}) {
  const resolve = pendingAskResolve;
  if (!resolve) return false;

  // Claim immediately: prevents a second submission from resolving the same ask.
  pendingAskResolve = undefined;

  const hasAttachments = !!deliverAttachments;
  if (hasAttachments) {
    await deliverAttachments(() => pendingAskResolve === resolve);
    // If attachments failed, fall back to echoing text or an error policy
    // (don’t leave the system in a “still waiting for answer” state).
  }

  setTurnPhase("streaming");
  resolve(prompt ?? "");
  return true;
}
```

Code sketch (capture target before background work)
```ts
const checkpointMsgIndex = messageStateHandler.getClineMessages()
  .findLastIndex(m => m.say === "checkpoint_created");
await say("checkpoint_created");
const targetIndex = messageStateHandler.getClineMessages().length - 1; // capture at creation

checkpointTracker.commit().then(commitHash => {
  // Update exactly the captured message (not “whatever is newest” now).
  void messageStateHandler.updateClineMessage(targetIndex, { lastCheckpointHash: commitHash });
});
```

Checklist for PRs in this area
- Do we set/clear the “pending”/resolver/slot state before any await?
- Does any background callback re-search for “the last” item instead of using a captured id/index?
- Are shared buffers/status maps protected by per-entity serialization or per-operation snapshots?
- On timeout/abort/early settlement, are we disconnecting/cancelling and cleaning listeners/pipes/timers?
- Are requests that can’t complete guaranteed to resolve (deadline + policy), not wait forever?