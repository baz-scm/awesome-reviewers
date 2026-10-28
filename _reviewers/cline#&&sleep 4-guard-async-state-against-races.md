---
title: Guard async state against races
description: A recurring class of bugs comes from async code that reads or acts on
  shared/mutable state across an `await` without re-validating that the state is still
  what it was when the operation started. Between the read and the resolution of the
  awaited work, another call, event, teardown, or retry can change that state, producing
  stale writes, double-handling,...
repository: cline/cline#&&sleep 4
label: Concurrency
language: TypeScript
comments_count: 16
repository_stars: 70980
---

A recurring class of bugs comes from async code that reads or acts on shared/mutable state across an `await` without re-validating that the state is still what it was when the operation started. Between the read and the resolution of the awaited work, another call, event, teardown, or retry can change that state, producing stale writes, double-handling, lost updates, or operating on a torn-down resource.

Apply these guards whenever an async operation spans a point where the relevant state could change concurrently:

1. **Claim before you await.** If an action must happen at most once (resolving a pending promise, taking a lock slot, consuming a queued item), commit to it synchronously — clear/mark the shared slot — before starting any async work (delivery, I/O, a network call). A later concurrent call must see the claim and fall back to another path instead of racing the same resolution.

```ts
// Wrong: another caller can see pendingAskResolve still set while we await.
async function resolve(prompt: string) {
  if (!pendingAskResolve) return false
  await deliverAttachments() // <-- window where a second caller resolves the same ask
  pendingAskResolve(prompt)
  pendingAskResolve = undefined
  return true
}

// Right: claim first, so a concurrent caller takes the follow-up path instead.
async function resolve(prompt: string) {
  const resolveFn = pendingAskResolve
  if (!resolveFn) return false
  pendingAskResolve = undefined
  await deliverAttachments()
  resolveFn(prompt)
  return true
}
```

2. **Stamp a generation/epoch and re-check it after every await.** When a long-running or resumable operation (a bound session, a served UI set, a rebuild) can be superseded, capture the current generation before starting, and discard the result if the generation has moved by the time the awaited work resolves. Bump the generation on unbind/cancel *before* the teardown step that could race a late reply, not after.

3. **Build the replacement before tearing down the original.** When replacing a resource under a shared key (a session runtime, a cached host, a plugin UI epoch), construct and register the new one first, and only release the old one once it has been displaced — guarded so release never evicts a live replacement. This avoids a window where the key resolves to nothing, or where a failed rebuild leaves the system without any resident resource.

4. **Serialize conflicting writers on the same key/entity.** When multiple call sites can act on the same mutable record concurrently (status writes, account switches, cache repopulation, host reload), chain the operations through a per-key promise queue rather than relying on the last write winning. Each link in the chain should re-read current state before acting, not trust what the caller observed before it queued.

5. **Prefer authoritative checks over time-based heuristics** for liveness/ownership decisions (e.g., "is this pid still running" over "was this heartbeat refreshed recently"), since staleness windows are a frequent source of races between legitimately slow operations and actually-abandoned state.

Every fix for this class of bug should come with a regression test that exercises the race directly (e.g., holds an awaited step open while a second caller or event arrives) rather than relying on timing alone.