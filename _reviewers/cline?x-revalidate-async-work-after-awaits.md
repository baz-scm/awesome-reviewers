---
title: Revalidate async work after awaits
description: 'Many bugs in this codebase come from async code that resumes after an
  `await` and blindly applies a side effect (mutating shared state, pushing a UI update,
  disposing a resource, scheduling a timer) without checking whether the world changed
  while it was suspended: a session was replaced, the user cancelled, a newer request
  superseded it, the account scope...'
repository: cline/cline?x
label: Concurrency
language: TypeScript
comments_count: 13
repository_stars: 70983
---

Many bugs in this codebase come from async code that resumes after an `await` and blindly applies a side effect (mutating shared state, pushing a UI update, disposing a resource, scheduling a timer) without checking whether the world changed while it was suspended: a session was replaced, the user cancelled, a newer request superseded it, the account scope changed, or the object was already torn down. Any operation that spans an await on behalf of a mutable, shared, or replaceable resource must capture a validity token (a generation/epoch counter, an `AbortSignal`, or a "still current" predicate) *before* its first await, and re-check that token immediately before every subsequent side effect — not just once at the end.

Practical rules:
- Bump a generation/epoch counter whenever the resource is replaced, cancelled, or torn down; capture the counter's value before starting async work and compare it after every await.
- When a newer operation can legitimately supersede an older one, make the older one a no-op on resume (dispose what it built, skip the write) rather than letting it race the newer one to completion.
- Never leave a "no resident/current object" gap: build the replacement first, swap it in, and only then release/dispose the old one, so every concurrent reader sees a valid resource throughout.
- When a resource may be reclaimed or disposed while in use by a long-lived read (e.g. status resolution, idle sweep), pin/ref-count it for the duration of that use instead of relying on it still being there afterward.
- For concurrent writers to the same piece of state, don't rely on "last write wins" from arrival order; serialize the writes (a per-key promise queue) or make the logically-authoritative writer (e.g. teardown) always win regardless of timing.

Example:
```ts
async function startReplacement(sessionId: string) {
  const generation = ++this.generation; // snapshot before any await
  const next = await buildRuntime(sessionId); // may yield for a while
  // The world may have moved on: a newer start, a cancel, or dispose.
  if (generation !== this.generation || this.disposed) {
    await next.dispose().catch(() => {});
    return;
  }
  const previous = this.sessions.get(sessionId);
  this.sessions.set(sessionId, next); // swap in before releasing old
  await previous?.release().catch(() => {});
}
```
Add a regression test for the race itself (start a second operation while the first is still pending, or dispose while a read is in flight) rather than only testing the happy path, since these windows are easy to reopen during later refactors.