---
title: Async Ownership and Ordering
description: Require every async side-effect to be tied to a specific owner (session/run/tab/question/task)
  with explicit ordering, cancellation, and validity checks, so late stragglers can’t
  overwrite newer state or leak resources.
repository: cline/cline#v2
label: Concurrency
language: TypeScript
comments_count: 12
repository_stars: 70861
---

Require every async side-effect to be tied to a specific owner (session/run/tab/question/task) with explicit ordering, cancellation, and validity checks, so late stragglers can’t overwrite newer state or leak resources.

Apply these rules:
1) Claim before awaiting: If multiple submissions/attempts can resolve the same logical item, set/claim the resolver synchronously (before any `await`) so only one attempt can “own” the resolution.
2) Invalidate with tokens/generations: For each owner-bound async flow, capture a token (generation id / execution id / start epoch) and, after each `await`, re-check that the token is still current before applying results.
3) Serialize shared writes per identity: If two async paths may write the same persisted/state row (or same in-memory slot), chain/serialize by identity (e.g., per session) so teardown/rollback lands last or in the intended order.
4) Make waits bounded and abort-aware: Any indefinite wait (disconnected clients, capability callbacks, retries/backoff, sleeps) must use deadlines and propagate `AbortSignal` so cancellation stops follow-on work.
5) Preserve “result-needed” async contracts: If downstream logic requires a computed value to be present, don’t remove `await`/decouple in a way that returns before the value is available (or serialize/chunk so required sequencing remains correct).
6) Clean up resources on early settlement: If you settle via fallback (timeouts/early resolve), ensure event listeners, pipes, timers, and other inherited resources are cleaned up so background work can’t keep the host alive or corrupt state.

Minimal pattern:
```ts
// Shared per-owner serialization (e.g., status persistence)
const perOwnerQueue = new Map<string, Promise<void>>();
function chainOwner(ownerId: string, fn: () => Promise<void>) {
  const prev = perOwnerQueue.get(ownerId) ?? Promise.resolve();
  const next = prev.then(fn, fn);
  perOwnerQueue.set(ownerId, next.then(() => undefined));
  return next;
}

async function runOwned(ownerId: string, signal: AbortSignal) {
  const generation = (ownerGen.get(ownerId) ?? 0) + 1;
  ownerGen.set(ownerId, generation);

  // Claim synchronously if resolving a single logical item
  // (example: resolver = resolveFn; resolveFn = undefined immediately)

  await someAsyncStep(signal);
  if (signal.aborted) return;
  if ((ownerGen.get(ownerId) ?? 0) !== generation) return; // stale

  await chainOwner(ownerId, async () => {
    // Apply ordered write(s) and guards here
    await persistStatus({ ownerId, generation });
  });
}
```

Use this checklist for code review: “Can a later async path overwrite an earlier one? Is there a token/claim + a stale check? Are shared writes ordered/serialized? Are waits bounded + abort-aware? Are required contracts preserved when removing awaits? Are listeners/pipes cleaned up on early settlement?”