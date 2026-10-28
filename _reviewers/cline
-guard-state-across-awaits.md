---
title: Guard state across awaits
description: Code that spans multiple `await` points (or kicks off background work)
  must not assume the state it captured before the first await is still true when
  it resumes. A map entry, flag, cached snapshot, buffer reference, or "who owns this"
  check can all change while a promise is pending, and letting the resumed code act
  on stale assumptions produces exactly the...
repository: "cline/cline\r\n"
label: Concurrency
language: TypeScript
comments_count: 25
repository_stars: 70946
---

Code that spans multiple `await` points (or kicks off background work) must not assume the state it captured before the first await is still true when it resumes. A map entry, flag, cached snapshot, buffer reference, or "who owns this" check can all change while a promise is pending, and letting the resumed code act on stale assumptions produces exactly the bugs seen repeatedly: a late write overwriting a newer one (status fields, fold snapshots, per-message hashes), a resource disposed or released while another in-flight call is still using it (MCP sessions, cloud hosts, plugin UI epochs, replaced session runtimes), duplicated or replayed work (concurrent plugin-host loads, overlapping commit generations), and callbacks or timers misattributed to the wrong caller after a reconnect/retry.

Apply this pattern whenever work crosses an await boundary and touches shared mutable state:
1. Capture an identity/generation token (an epoch counter, the specific object reference, a "which attempt is this" id) before the first await.
2. After every subsequent await, re-check that token against current state before mutating anything or acting on the result. If it no longer matches, bail out instead of overwriting/acting.
3. When multiple operations can legitimately target the same resource, serialize them explicitly (chain onto one promise/queue per key) rather than letting them race and hoping the last one wins correctly.
4. When a resource might still be in use by another in-flight operation, pin/reference-count it for the duration of that use so a concurrent idle-sweep, teardown, or rebuild cannot release it out from under the active caller.

Example of the re-check pattern:

```ts
async function doWork(key: string) {
  const token = currentGeneration(key); // snapshot before any await
  const data = await fetchSomething();
  if (currentGeneration(key) !== token) {
    return; // state moved on while we were awaiting; our result is stale
  }
  applyResult(key, data);
}
```

Prefer this re-validation over ad hoc locks or "hope it doesn't happen" reasoning, and add a regression test that holds one async step open while a second, conflicting operation runs to completion, asserting the earlier one does not clobber or act on behalf of the later one.