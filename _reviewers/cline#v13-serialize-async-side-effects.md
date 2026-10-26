---
title: Serialize Async Side Effects
description: When async work targets shared state (status rows, queues, listeners,
  persisted checkpoints, cached hosts), races happen at overlaps and “late promises”
  overwrite invariants. Standardize concurrency so ownership is explicit, side effects
  are serialized per key, and cancellation/cleanup are guaranteed.
repository: cline/cline#v13
label: Concurrency
language: TypeScript
comments_count: 11
repository_stars: 70874
---

When async work targets shared state (status rows, queues, listeners, persisted checkpoints, cached hosts), races happen at overlaps and “late promises” overwrite invariants. Standardize concurrency so ownership is explicit, side effects are serialized per key, and cancellation/cleanup are guaranteed.

**Do this:**
1) **Serialize per shared key** (sessionId/taskId/hostKey). Chain writes on a per-key promise queue so teardown/terminal states can’t be overwritten.
2) **Claim ownership before awaiting** any async step that must be “single-resolve” (e.g., pending question, request routing). Don’t let a second submission resolve the same pending work while you’re preparing attachments or other side effects.
3) **Re-check conditions at the last safe boundary** after acquiring locks / switching turns. If eligibility can change concurrently, validate *right before* the state-changing operation.
4) **Use deadlines for unanswerable waits**. If the responder can disconnect/detach, fail immediately and/or apply capability-specific timeouts.
5) **Cleanup on settlement**. If you settle a promise via timeout/fallback, also remove listeners, close/stop inherited pipes, and prevent background children from keeping the host alive.

**Example: claim-before-await (single-resolve)**
```ts
const resolve = pendingAskResolve;
if (!resolve) return false;
// Claim first, so no second submission can resolve the same question.
pendingAskResolve = undefined;

const hasAttachments = (images?.length ?? 0) > 0 || (files?.length ?? 0) > 0;
if (hasAttachments && deliverAttachments) {
  await deliverAttachments(() => pendingAskResolve === undefined);
  // If delivery fails, fall back to replying with text as your app requires.
}
setTurnPhase('streaming');
resolve(prompt ?? '');
return true;
```

**Example: per-key serialization (terminal state wins)**
```ts
const queues = new Map<string, Promise<void>>();
function enqueue(key: string, work: () => Promise<void>) {
  const prev = queues.get(key) ?? Promise.resolve();
  const next = prev.then(work).finally(() => {
    if (queues.get(key) === next) queues.delete(key);
  });
  queues.set(key, next);
  return next;
}

await enqueue(sessionId, async () => {
  if (sessionShuttingDown && isNonTerminalStatus(status)) return;
  await persistence.updateStatus(sessionId, status);
});
```

Use these patterns for any flow where overlapping promises can: (a) write shared state, (b) decide routing/eligibility, (c) register handlers, or (d) depend on ordering invariants. Combine with timeouts and settlement cleanup to avoid leaks and indefinite waits.