---
title: Claim Work Before Await
description: 'When correctness depends on order/ownership, do two things: (1) “claim”
  the right to update synchronously before the first `await`, and (2) capture the
  exact target you will update before any async work.'
repository: cline/cline#v30
label: Concurrency
language: TypeScript
comments_count: 13
repository_stars: 70894
---

When correctness depends on order/ownership, do two things: (1) “claim” the right to update synchronously before the first `await`, and (2) capture the exact target you will update before any async work.

Practical rules:
- **Claim ownership before awaiting**: If there is a “pending operation” (e.g., pending ask-question resolution, single completion winner), set/clear the owner immediately, then run async delivery/side-effects.
- **Capture targets immediately**: If you create a record/message and later annotate it, capture the index/id returned by that synchronous creation step. Don’t “re-find the latest” after an awaited commit—commits can resolve out of order.
- **Guard async with “currentness” tokens**: For shared state transitions (rebuilds, session replacement, refresh caches), require an explicit generation/version check before committing results.
- **Use cancellation/timeouts + cleanup**: If an async operation can outlive its use (timeouts, late subprocess hooks, late network connects), ensure late work either self-aborts via `AbortSignal`/deadline or cleans up resources so it can’t mutate state after teardown.

Example (claim + capture target):
```ts
// Claim synchronously, before awaiting any delivery.
async function resolvePendingAsk(params: {
  prompt?: string;
  deliverAttachments?: () => Promise<void>;
}) {
  const resolve = pendingAskResolve;
  if (!resolve) return false;

  // Claim now; late contenders will fall through.
  pendingAskResolve = undefined;

  const echoText = params.prompt ?? "";
  if (params.deliverAttachments) {
    await params.deliverAttachments();
  }

  setTurnPhase("streaming");
  resolve(echoText);
  return true;
}

// Capture exact message index right after creation.
async function checkpointCreatedAndAnnotate(createMessage: () => Promise<number>, commit: () => Promise<string | undefined>) {
  const createdMsgIndex = await createMessage(); // synchronous boundary: capture now
  const commitHash = await commit();
  if (!commitHash) return;
  await updateMessage(createdMsgIndex, { lastCheckpointHash: commitHash });
}
```

Adopting this standard prevents the common concurrency bugs seen here: stale callbacks winning, out-of-order async updates corrupting state, late resources keeping processes alive, and teardown races overwriting newer transitions.