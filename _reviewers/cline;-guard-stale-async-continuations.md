---
title: Guard stale async continuations
description: 'A huge class of concurrency bugs in this codebase comes from async work
  (an RPC, a connect, a file read, a rebuild) resolving after the state it was launched
  against has moved on: the session rebound to another id, the pane unmounted, the
  account/scope changed, a newer request superseded it, or the resource was torn down.
  Applying that stale result anyway...'
repository: cline/cline;
label: Concurrency
language: TypeScript
comments_count: 20
repository_stars: 70964
---

A huge class of concurrency bugs in this codebase comes from async work (an RPC, a connect, a file read, a rebuild) resolving after the state it was launched against has moved on: the session rebound to another id, the pane unmounted, the account/scope changed, a newer request superseded it, or the resource was torn down. Applying that stale result anyway causes leaked connections, UI showing another session's data, double-sends, lost cancellations, or corrupted shared state.

Treat every `await` as a point where the world may have changed, and make the code defend against it explicitly:

1. **Capture identity/generation before awaiting, not after.** Snapshot the session id, bind/account/scope generation, or an abort signal synchronously before the first `await`, so a concurrent change can't be attributed to the wrong request.
2. **Bump a generation/epoch counter on every rebind, cancel, or scope change**, and have in-flight work re-check it (`generation === this.generation`, `isCurrent()`, `!isStale()`) immediately after each `await` before mutating shared state, dispatching results, or starting the next step. If stale, discard the result (and release any resource it acquired) instead of applying it.
3. **When a cheap generation check isn't enough to prevent corruption** (e.g. two writers racing on the same file, record, or in-flight call), serialize the operations explicitly: a mutex/`runExclusive`, a per-key queue, atomic rename-and-compare-before-delete, or claiming a slot synchronously before any await.
4. **Never let cleanup silently no-op on the stale path.** A superseded start, cancelled fetch, or unmounted binding must still dispose connections/hosts/timers it created; "stale" means "ignore the result," not "skip teardown."
5. **Cancellation must reach every in-flight waiter**, not just the one holding the current reference — e.g. aborting a pending start should cancel turns queued behind it too, and a Stop action should cancel *every* concurrently running operation it owns, not just the most recently started one.

Example shape, generalized from several fixes in this codebase:

```ts
async function connect(entry: Entry): Promise<Host> {
  const generation = this.scopeGeneration;         // capture before awaiting
  const host = await Host.connect(entry.config);    // the world can change here
  if (this.disposed || generation !== this.scopeGeneration || this.entries.get(entry.id) !== entry) {
    await host.dispose("superseded").catch(() => undefined); // never skip cleanup
    throw new Error("connection was superseded");
  }
  entry.host = host; // safe: still current
  return host;
}
```

Add a regression test for the race itself (hold one async step pending, trigger the invalidating event, release, assert the stale branch is taken) — most of the fixes referenced here were only caught because such a test was written.