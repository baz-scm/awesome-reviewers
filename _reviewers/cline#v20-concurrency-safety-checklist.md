---
title: Concurrency Safety Checklist
description: Use explicit “async ownership” to keep late/overlapping tasks from corrupting
  newer state, and ensure every timeout/cancellation path releases resources.
repository: cline/cline#v20
label: Concurrency
language: TypeScript
comments_count: 10
repository_stars: 70886
---

Use explicit “async ownership” to keep late/overlapping tasks from corrupting newer state, and ensure every timeout/cancellation path releases resources.

**Rules**
1. **Claim before awaiting** for single-consumer actions (answers, approvals, pending tasks). Resolve/clear the shared promise/claim synchronously *before* any await/IO.
2. **Gate late callbacks**: attach a `generation`/`attemptId`/`sessionId` token to each async operation; when it completes, apply effects only if the token is still current.
3. **Capture the target synchronously**: if you must do background work, identify the exact object/slot (index/id/messageId) *before* the await, then update exactly that captured target. Never “re-find the latest” after concurrency.
4. **Timeouts must clean up**: if a deadline wins over an in-flight promise, the eventual late completion must still trigger cleanup (disconnect/close/unsubscribe/dispose). Timeouts should not leave live connections, pipes, or timers behind.
5. **Serialize ordered shared writes**: if overlapping writes can occur (teardown vs running), chain them per key so the intended order always “lands last”.
6. **Concurrency caps must cap in-flight, not total**: when limiting parallelism, ensure extra workers continue fetching new work until the queue is drained.

**Patterns**
- *Claim-before-await*:
```ts
const resolve = pendingResolve;
if (!resolve) return false;
pendingResolve = undefined; // claim now
if (hasAttachments) {
  await deliverAttachments();
  return true;
}
resolve(promptText ?? "");
return true;
```
- *Generation gate + cleanup*:
```ts
const gen = ++currentGen;
const result = await longOp();
if (gen !== currentGen) {
  cleanupLate(result); // close/disconnect
  return;
}
apply(result);
```
- *Capture target before background commit*:
```ts
await say("checkpoint_created");
const messageIndex = findLastIndex(messages, m => m.say === "checkpoint_created");
const commitHash = await commit();
if (messageIndex !== -1 && messages[messageIndex]?.say === "checkpoint_created") {
  updateClineMessage(messageIndex, { lastCheckpointHash: commitHash });
}
```
- *Timeout with late disconnect*:
```ts
const timeout = setTimeout(() => timedOut = true, ms);
try {
  await connectPromise;
} finally {
  if (timedOut) await disconnect();
  clearTimeout(timeout);
}
```

Apply this checklist whenever you see: shared mutable state touched after `await`, background work kicked off without capturing the correct target, or timeouts/cancellation that don’t explicitly dispose connections/pipes/listeners.