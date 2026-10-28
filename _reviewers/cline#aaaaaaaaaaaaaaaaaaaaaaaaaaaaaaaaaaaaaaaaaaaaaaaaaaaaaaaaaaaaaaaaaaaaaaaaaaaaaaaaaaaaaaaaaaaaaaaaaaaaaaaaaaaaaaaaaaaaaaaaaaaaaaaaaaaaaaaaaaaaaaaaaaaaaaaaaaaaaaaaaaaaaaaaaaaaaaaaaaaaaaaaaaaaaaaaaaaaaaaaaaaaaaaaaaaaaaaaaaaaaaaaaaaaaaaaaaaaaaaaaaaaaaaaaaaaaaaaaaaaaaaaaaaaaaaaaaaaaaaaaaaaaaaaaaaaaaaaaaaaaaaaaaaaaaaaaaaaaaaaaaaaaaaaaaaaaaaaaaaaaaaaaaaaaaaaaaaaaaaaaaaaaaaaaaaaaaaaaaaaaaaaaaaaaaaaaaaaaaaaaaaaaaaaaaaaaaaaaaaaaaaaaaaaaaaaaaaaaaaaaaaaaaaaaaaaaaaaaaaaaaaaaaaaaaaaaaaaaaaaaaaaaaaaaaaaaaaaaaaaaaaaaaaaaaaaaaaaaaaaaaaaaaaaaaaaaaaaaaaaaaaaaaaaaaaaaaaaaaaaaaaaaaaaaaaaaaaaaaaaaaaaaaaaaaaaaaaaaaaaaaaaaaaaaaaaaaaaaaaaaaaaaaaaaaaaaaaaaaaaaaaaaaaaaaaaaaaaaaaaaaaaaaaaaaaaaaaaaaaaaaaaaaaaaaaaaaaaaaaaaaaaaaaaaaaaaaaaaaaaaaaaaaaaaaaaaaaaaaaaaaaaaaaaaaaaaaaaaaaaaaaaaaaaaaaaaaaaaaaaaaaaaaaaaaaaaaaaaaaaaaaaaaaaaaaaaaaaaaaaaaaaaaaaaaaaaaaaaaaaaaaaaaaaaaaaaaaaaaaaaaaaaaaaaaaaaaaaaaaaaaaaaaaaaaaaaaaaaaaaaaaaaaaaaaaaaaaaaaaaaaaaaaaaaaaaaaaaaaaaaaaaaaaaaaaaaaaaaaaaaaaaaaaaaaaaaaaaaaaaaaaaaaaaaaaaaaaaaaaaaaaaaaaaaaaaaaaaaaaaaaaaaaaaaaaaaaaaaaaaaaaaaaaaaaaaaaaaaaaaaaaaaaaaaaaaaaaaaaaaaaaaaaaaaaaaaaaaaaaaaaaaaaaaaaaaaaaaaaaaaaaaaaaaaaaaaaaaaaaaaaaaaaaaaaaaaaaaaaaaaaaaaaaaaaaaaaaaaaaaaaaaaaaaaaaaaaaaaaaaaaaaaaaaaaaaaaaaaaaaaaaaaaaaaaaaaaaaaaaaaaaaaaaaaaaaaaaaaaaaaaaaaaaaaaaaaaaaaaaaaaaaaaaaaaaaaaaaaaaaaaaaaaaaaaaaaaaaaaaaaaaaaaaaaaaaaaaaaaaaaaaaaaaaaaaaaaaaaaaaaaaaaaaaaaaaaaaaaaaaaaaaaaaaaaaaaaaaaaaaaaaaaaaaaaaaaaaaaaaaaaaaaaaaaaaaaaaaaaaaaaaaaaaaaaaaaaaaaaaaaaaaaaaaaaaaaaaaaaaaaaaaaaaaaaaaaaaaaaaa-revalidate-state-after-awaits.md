---
title: Revalidate state after awaits
description: 'A huge share of concurrency bugs in this codebase come from the same
  shape: code reads a shared mutable resource (a map slot, a cached connection, a
  flag, a counter), does an `await`, and then acts on what it read as if nothing could
  have changed in between. In reality another call, a teardown, a reload, or a cancellation
  can run during that gap and...'
repository: cline/cline#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
label: Concurrency
language: TypeScript
comments_count: 20
repository_stars: 70965
---

A huge share of concurrency bugs in this codebase come from the same shape: code reads a shared mutable resource (a map slot, a cached connection, a flag, a counter), does an `await`, and then acts on what it read as if nothing could have changed in between. In reality another call, a teardown, a reload, or a cancellation can run during that gap and replace, release, or invalidate the thing just read. Acting on the stale reference then clobbers newer state, double-releases a live resource, drops a still-needed write, or resolves the wrong request.

The fix is always the same shape: capture an identity/version for what you're about to act on *before* the await (the object reference itself, or an explicit generation/epoch counter), and re-check immediately after the await — right before the mutating side effect — that it is still current. If it isn't, skip, discard, or retry instead of overwriting/releasing what is now there. Do this at every await boundary that separates "decide" from "act", not just the first one; a second unguarded await after the check reopens the same race.

```ts
async function replaceResource(id: string, build: () => Promise<Resource>): Promise<void> {
  const previous = registry.get(id)
  const next = await build() // another replace/teardown can run while this awaits
  if (registry.get(id) !== previous) {
    // the slot moved on without us; don't clobber or double-release it
    await next.dispose().catch(() => undefined)
    return
  }
  registry.set(id, next)
  await previous?.dispose().catch(() => undefined)
}
```

Apply this pattern whenever you:
- replace or release a session/connection/host that lives in a shared map (guard the release with "is this slot still mine?"),
- resolve a pending request/promise that a later caller might also try to resolve (claim it synchronously before any await),
- persist a result computed from a snapshot (model id, config, scope) that could have been superseded meanwhile,
- tear down or finalize work after a cancellation/dispose signal may have fired mid-await,
- write into a cache or file after a stat/check whose result can go stale before the write lands.

Prefer reference-identity or monotonic generation/epoch checks over timestamps or heuristics (e.g., staleness windows, "last write wins" without a check) — heuristics degrade under load or slow I/O and reintroduce the same race under different timing. When multiple concurrent callers must not interleave at all, serialize them explicitly (chain onto the in-flight promise, or use an exclusive-run queue) rather than relying solely on post-await checks.