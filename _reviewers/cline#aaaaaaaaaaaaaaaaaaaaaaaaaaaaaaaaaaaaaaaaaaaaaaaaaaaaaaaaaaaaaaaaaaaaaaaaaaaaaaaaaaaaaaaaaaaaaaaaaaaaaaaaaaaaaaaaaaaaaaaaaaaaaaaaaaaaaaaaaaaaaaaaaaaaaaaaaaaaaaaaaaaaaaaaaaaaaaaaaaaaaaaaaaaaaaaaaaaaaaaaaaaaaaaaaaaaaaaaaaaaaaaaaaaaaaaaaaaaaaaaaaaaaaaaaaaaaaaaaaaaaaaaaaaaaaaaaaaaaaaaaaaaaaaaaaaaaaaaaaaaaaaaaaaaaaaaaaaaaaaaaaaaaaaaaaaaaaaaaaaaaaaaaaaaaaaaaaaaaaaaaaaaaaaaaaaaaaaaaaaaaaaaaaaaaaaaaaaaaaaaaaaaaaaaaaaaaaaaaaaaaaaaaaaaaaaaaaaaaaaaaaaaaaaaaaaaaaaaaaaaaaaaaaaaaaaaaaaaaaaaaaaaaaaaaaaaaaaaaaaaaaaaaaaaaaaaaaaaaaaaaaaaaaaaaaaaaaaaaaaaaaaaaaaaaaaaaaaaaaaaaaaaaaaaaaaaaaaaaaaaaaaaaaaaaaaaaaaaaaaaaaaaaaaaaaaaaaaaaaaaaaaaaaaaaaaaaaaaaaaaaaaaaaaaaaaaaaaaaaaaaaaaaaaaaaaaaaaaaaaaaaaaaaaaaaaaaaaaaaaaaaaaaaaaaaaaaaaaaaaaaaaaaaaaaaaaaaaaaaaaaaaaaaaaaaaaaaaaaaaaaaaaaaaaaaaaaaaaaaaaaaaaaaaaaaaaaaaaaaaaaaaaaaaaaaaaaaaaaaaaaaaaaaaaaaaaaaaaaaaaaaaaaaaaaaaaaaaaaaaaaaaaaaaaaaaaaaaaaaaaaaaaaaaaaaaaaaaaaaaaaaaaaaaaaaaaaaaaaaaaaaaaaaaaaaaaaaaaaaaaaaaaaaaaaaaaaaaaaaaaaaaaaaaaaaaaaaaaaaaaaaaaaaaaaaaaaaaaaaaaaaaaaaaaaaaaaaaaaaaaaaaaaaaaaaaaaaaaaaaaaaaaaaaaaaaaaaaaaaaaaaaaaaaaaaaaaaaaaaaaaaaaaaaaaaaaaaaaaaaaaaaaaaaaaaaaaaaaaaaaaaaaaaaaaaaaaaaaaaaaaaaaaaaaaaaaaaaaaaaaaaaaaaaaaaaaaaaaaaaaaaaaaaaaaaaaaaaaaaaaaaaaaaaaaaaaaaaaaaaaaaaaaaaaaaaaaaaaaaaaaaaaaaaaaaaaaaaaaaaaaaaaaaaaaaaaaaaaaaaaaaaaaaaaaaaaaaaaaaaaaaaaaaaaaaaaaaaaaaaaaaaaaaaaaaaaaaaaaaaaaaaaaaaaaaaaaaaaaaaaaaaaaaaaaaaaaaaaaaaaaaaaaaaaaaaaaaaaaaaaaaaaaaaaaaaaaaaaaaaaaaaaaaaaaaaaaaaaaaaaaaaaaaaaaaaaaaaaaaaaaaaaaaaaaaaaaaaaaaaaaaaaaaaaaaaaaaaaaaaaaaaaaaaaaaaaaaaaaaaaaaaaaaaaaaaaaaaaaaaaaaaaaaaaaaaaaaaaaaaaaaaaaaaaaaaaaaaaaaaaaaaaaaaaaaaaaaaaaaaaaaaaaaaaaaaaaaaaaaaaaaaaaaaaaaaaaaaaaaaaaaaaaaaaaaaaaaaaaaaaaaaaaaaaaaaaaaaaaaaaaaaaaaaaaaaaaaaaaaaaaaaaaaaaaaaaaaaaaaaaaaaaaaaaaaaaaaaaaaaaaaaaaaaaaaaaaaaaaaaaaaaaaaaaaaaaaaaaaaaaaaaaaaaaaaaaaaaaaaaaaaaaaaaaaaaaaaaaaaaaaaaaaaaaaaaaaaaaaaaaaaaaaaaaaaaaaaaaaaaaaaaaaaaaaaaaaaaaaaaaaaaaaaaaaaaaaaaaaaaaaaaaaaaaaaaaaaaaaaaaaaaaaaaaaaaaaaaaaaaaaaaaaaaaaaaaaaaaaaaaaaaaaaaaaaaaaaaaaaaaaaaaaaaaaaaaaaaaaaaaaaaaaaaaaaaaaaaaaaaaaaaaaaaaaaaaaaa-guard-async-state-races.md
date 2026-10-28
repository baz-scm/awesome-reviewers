---
title: Guard async state races
description: 'A large share of concurrency bugs in this codebase come from async work
  that spans one or more `await`s while the state it started with (a session, a question,
  an account scope, a connection, a pending start) can change underneath it: the caller
  is torn down, superseded, cancelled, or a second request for the same thing arrives.
  Treat every multi-step async...'
repository: cline/cline#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
label: Concurrency
language: TypeScript
comments_count: 36
repository_stars: 70973
---

A large share of concurrency bugs in this codebase come from async work that spans one or more `await`s while the state it started with (a session, a question, an account scope, a connection, a pending start) can change underneath it: the caller is torn down, superseded, cancelled, or a second request for the same thing arrives. Treat every multi-step async operation as potentially stale after each await, and design explicitly for that:

1. **Snapshot identity/generation before any await.** Capture a reference to the object you're operating on (not just an id) or a monotonically increasing generation/epoch counter before starting async work. After every subsequent await, re-check that the captured reference/generation is still current before applying side effects (writes, emitting events, resolving promises, installing UI state). If it isn't, stop — don't apply stale results.

```ts
const generation = this.generation;
const target = this.current;
const result = await doWork();
if (generation !== this.generation || this.current !== target) {
  return; // superseded; this result belongs to a reality that no longer exists
}
apply(result);
```

2. **Claim shared, one-shot resources synchronously, before awaiting.** When two concurrent callers could race to resolve the same pending request (an `ask_question`, a reconnect slot, a journal entry), clear/claim it in the same synchronous tick you decide to handle it — not after an awaited delivery step. Otherwise a second caller can observe the same "pending" state and double-resolve or steal it.

3. **Serialize or coalesce operations on the same key instead of letting them race.** When concurrent writes/starts/switches target the same resource (status writes, account switches, plugin host (re)loads, hub reconnect probes), chain them on a single promise/queue per key so each one sees the effect of the one before it, or coalesce repeated requests that arrive while one is in flight into a single rerun with fresh inputs — never let two writers race to "win" with whichever happens to finish last.

4. **Track in-flight work explicitly so teardown/cancellation is deterministic.** Don't infer "is something still running" indirectly (e.g., re-deriving it from unrelated flags); keep an explicit counter/promise/flag per unit of in-flight work (`turnsInFlight`, `pendingStart`, `scopeOperations`) that teardown, cancellation, and status transitions can await, abort, or check against, so cleanup never races the work it's supposed to wait for or cancel.

Apply these patterns any time code does `await` and then mutates shared state, resolves a shared callback, or decides whether to start new work — the question to always ask is "what could have changed while I was awaiting, and have I checked for it?"