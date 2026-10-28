---
title: Guard stale async state
description: 'Async code that checks a condition, awaits, then acts on it is prone
  to TOCTOU races: anything can change while the await is pending (a session rebuild,
  a tab close, a cancellation, a competing request). Treat every await as a point
  where your pre-conditions may have gone stale, and guard against it with two complementary
  techniques:'
repository: cline/cline#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
label: Concurrency
language: TypeScript
comments_count: 18
repository_stars: 70964
---

Async code that checks a condition, awaits, then acts on it is prone to TOCTOU races: anything can change while the await is pending (a session rebuild, a tab close, a cancellation, a competing request). Treat every await as a point where your pre-conditions may have gone stale, and guard against it with two complementary techniques:

1. Stamp a generation/epoch counter (or a per-operation token) when the operation starts, capture it before the first await, and re-check it immediately after each subsequent await before mutating shared state or applying the result. If it no longer matches, drop the result silently instead of applying it.

```ts
const generation = ++this.generation;
const result = await doWork();
if (generation !== this.generation) return; // superseded; discard
this.apply(result);
```

2. When a shared resource (a pending resolver, a session slot, a request record) must be handed to exactly one caller, claim/lock it synchronously before doing any async work, not after it completes. Claiming late lets a second concurrent caller grab the same resource while the first is still awaiting.

```ts
const resolve = this.pendingResolve;
if (!resolve) return false;
this.pendingResolve = undefined; // claim immediately; no one else can double-answer
await deliverAttachments();
resolve(responseText);
```

Favor serializing genuinely conflicting operations (status writes, account switches, rebuilds) through a queue/lock rather than letting them race and trusting the "last write wins," since the last writer to finish is not necessarily the most recent or most correct one. When adding any new await in code that reads-then-writes shared/mutable state, ask explicitly: "what could have changed while I was waiting, and have I re-checked for it?" Add a regression test that holds the await open (via a controllable promise) and injects the competing event to prove the guard actually fires.