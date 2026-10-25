---
title: Async race ownership rules
description: 'When multiple async operations can overlap with replacement/teardown
  (UI unmount, session rebuild, polling vs actions, stop/dispose, in-flight RPCs),
  require explicit *ownership* and *lifecycle binding*:'
repository: CLINE/CLINE
label: Concurrency
language: TypeScript
comments_count: 9
repository_stars: 70837
---

When multiple async operations can overlap with replacement/teardown (UI unmount, session rebuild, polling vs actions, stop/dispose, in-flight RPCs), require explicit *ownership* and *lifecycle binding*:

1) Claim ownership synchronously before the first await
- If there is a “pending” operation that others can also resolve (e.g., pending question/answer), assign/consume the claim immediately, then await delivery.
- This prevents a second submission from resolving the same pending item while the first is mid-await.

2) Bind every async result to an identity token (generation / requestId / sessionId / tabId)
- Capture a token at the start of the async operation.
- Before mutating shared state, verify the token still matches the current owner (or that the resource is still alive and not disposed).

3) Serialize or coalesce work per scope
- For recurring reads (polling) and triggers (actions, refresh reasons), ensure only one inflight request per (resource, scope) runs at a time.
- If a change happens while inflight, remember it and run exactly once more after the current request completes.

4) Cancellation-aware completion + deterministic cleanup
- If callers can cancel/stop/teardown, make sure cancellation is observed during waits/sleeps and that cleanup (listeners, inherited pipes, timers) happens when the caller settles.

Code sketch (claim-before-await + generation + serial coalescing)
```ts
let pending: null | (() => void) = null;
let pendingToken = 0;
let lastApplied = 0;

async function resolvePendingWithAttachments(
  tokenAtCall: number,
  deliver: () => Promise<void>,
): Promise<boolean> {
  const resolve = pending;
  if (!resolve) return false;

  // Claim synchronously
  pending = null;
  const myToken = ++pendingToken;

  try {
    await deliver();
    // Bind to identity: only apply if still current
    if (myToken !== pendingToken) return true;
    lastApplied = tokenAtCall;
    resolve();
    return true;
  } catch {
    // Release the claim if delivery fails so retries can happen
    if (myToken === pendingToken) pending = resolve;
    throw;
  }
}

// Polling/action coalescing pattern
let inflight: Promise<void> | null = null;
let rerunRequested = false;

async function refresh(reason: string) {
  if (!enabled) return;
  if (inflight) { rerunRequested = true; return; }
  inflight = (async () => {
    do {
      rerunRequested = false;
      const currentReason = reason;
      const response = await fetchState(currentReason);
      apply(response); // only after request completes
    } while (rerunRequested);
  })();
  try { await inflight; } finally { inflight = null; }
}
```

Adopting this standard prevents: 
- late stragglers overwriting current state,
- replacement requests “stealing” pending resolution,
- polls/actions returning out-of-order results,
- teardown leaving leaked resources (timers/pipes/listeners) alive after the caller is done.