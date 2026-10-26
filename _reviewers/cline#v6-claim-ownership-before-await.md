---
title: Claim Ownership Before Await
description: When async operations overlap, treat “who owns this result/side effect”
  as a critical invariant. Establish ownership synchronously (or serialize writers
  per key), then validate that ownership before applying any state after awaits.
repository: cline/cline#v6
label: Concurrency
language: TypeScript
comments_count: 8
repository_stars: 70864
---

When async operations overlap, treat “who owns this result/side effect” as a critical invariant. Establish ownership synchronously (or serialize writers per key), then validate that ownership before applying any state after awaits.

Practical rules:
1) Claim before await: if a function resolves a pending action (ask/question, reply, status transition, checkpoint association), assign/claim the pending token synchronously, then start awaiting work.
2) Generation/phase guards: capture a generation/attempt id (bind generation, attempt token, plugin generation) at the start of the async flow and re-check it before dispatching state.
3) Serialize side effects per entity: if multiple writers can update the same row/buffer/status, chain writes (or use a per-key mutex/queue) so teardown/terminal transitions cannot be overwritten by an in-flight operation.
4) Don’t mutate after disposal/retirement: before writing to state tied to a lifetime (disposed xterm tab, released plugin copy, torn-down session), confirm the same generation/owner is still current.
5) Abort/deadline + cleanup: ensure overlapping work respects abort signals, merges in-flight reads/waits, and cleans up timers/listeners/pipes so promises can’t hang.

Code pattern (claim-before-await + guard):
```ts
// Bad: awaiting first allows a second submission to win/replace.
const resolve = pending;
await deliverAttachments();
if (resolve) resolve(text);

// Good: claim immediately, then await, then apply only if still current.
const resolve = pending;
if (!resolve) return false;
pending = undefined; // or bump generation token
const myResolve = resolve;
try {
  if (hasAttachments) await deliverAttachments(() => pending === undefined);
  // After awaits, do not apply if a newer attempt superseded this one
  if (myResolve !== resolve /* or generation mismatch */) return false;
  setTurnPhase('streaming');
  myResolve(prompt ?? '');
  return true;
} catch (e) {
  // Release only your own claim; never leave the system suspended.
  return true;
}
```

Adopt this as a review checklist for any handler that can run concurrently: (a) what key owns the result, (b) is it claimed/serialized before the first await, and (c) do we re-check ownership before mutating shared state?
