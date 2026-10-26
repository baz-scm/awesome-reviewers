---
title: Async Concurrency Discipline
description: 'When working concurrently (promises, retries, UI lifecycle, background
  tasks, subprocesses), apply a consistent discipline:


  1) **Gate async results with an “ownership token”**'
repository: cline/cline#v27
label: Concurrency
language: TypeScript
comments_count: 13
repository_stars: 70892
---

When working concurrently (promises, retries, UI lifecycle, background tasks, subprocesses), apply a consistent discipline:

1) **Gate async results with an “ownership token”**
- Maintain a per-operation/ per-binding **generation/epoch id**.
- Only apply results if the token is still current; otherwise discard (or close/undo the work).

2) **Claim shared intent before the first await**
- For one-shot decisions (answers, transitions, capability callbacks), set/clear the shared state *synchronously* before awaiting delivery. This prevents overlap where a second request “resolves” the same slot.

3) **Make teardown ordering explicit (serialize teardown last)**
- If teardown must win (e.g., cancel vs running, session dispose vs afterRun), **chain writes/updates** so teardown can’t be overwritten by in-flight transitions.

4) **Bound waits and handle “owner gone” paths**
- Every wait should have a **timeout** or be cancelled when the owner unregisters/disposes, otherwise you can deadlock forever.

5) **Cleanup after settling, not only on success**
- When promises resolve/reject, use `finally` to clear timers, listeners, and inherited resources (stdio pipes, intervals). Don’t rely on child cleanup that may be delayed by background grandchildren.

Minimal pattern (ownership token + claim-before-await + cleanup):
```ts
let generation = 0;
let claimed: (() => void) | undefined;

function startBinding() {
  const myGen = ++generation;
  return async () => {
    // Claim-before-await
    const resolveClaim = claimed;
    claimed = undefined;
    try {
      const result = await doAsyncWork();
      if (myGen !== generation) return; // discard stale result
      resolveClaim?.();
    } finally {
      // cleanup always
      cleanupTimersAndListeners();
    }
  };
}
```

Apply these rules anywhere you see: timeouts/deadlines, retries, out-of-order resolves, UI unmount/rebind, session replacement, or background/subprocess work. This prevents the recurring failures shown here: late async applying to retired state, overlapping one-shot decisions, teardown getting overwritten, hangs after owner removal, and resource leaks keeping processes alive.