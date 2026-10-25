---
title: Async ownership and cleanup
description: 'When async work outlives its creator, late completions/callbacks will
  corrupt the current state (wrong session, double-send, lost attachments, teardown
  overwritten). Standardize concurrency ownership and cleanup:'
repository: ClInE/cLiNe
label: Concurrency
language: TypeScript
comments_count: 8
repository_stars: 70838
---

When async work outlives its creator, late completions/callbacks will corrupt the current state (wrong session, double-send, lost attachments, teardown overwritten). Standardize concurrency ownership and cleanup:

1) Guard every awaited continuation with an ownership token
- Use a monotonic generation/attempt id stored in a ref/closure.
- Increment generation on (re)bind/restart/cleanup.
- After any await, re-check the current generation (or “still starting”/“still running” state) before mutating shared state.

2) Claim before await for single-consumer promises
- If multiple events could resolve the same pending request, “claim” it (set to undefined / mark consumed) before awaiting attachment delivery or other async steps.

3) Avoid stacking side effects on retries
- Register event listeners once at creation; route their handling through the current owned state (e.g., tab.pty, status, or a generation-valid reference).
- Retried start/spawn must not add new listeners.

4) Serialize ordering-sensitive writes per key
- For state machines where “shutdown/teardown must win”, chain writes or guard with session shutdown flags so late in-flight transitions can’t overwrite the terminal status.

5) Clean up resources immediately on settle (including fallbacks)
- After resolving/rejecting due to timeout/fallback, remove/detach inherited listeners/pipes/timers so background children or late outputs can’t keep the host alive or accumulate output.

Example pattern (generation guard + claim-before-await)
```ts
let generation = 0;
const current = () => generation;

function rebind() {
  generation += 1;
  const g = current();

  (async () => {
    const reply = await getReply();
    if (g !== current()) return; // ownership check
    applyReplyToLiveState(reply);
  })();

  return () => {
    generation += 1; // invalidates pending continuations
  };
}

// Single-consumer claim before await
let pendingResolve: ((value: string) => void) | undefined;
async function resolveOnce() {
  const resolve = pendingResolve;
  if (!resolve) return;
  pendingResolve = undefined; // claim

  await deliverAttachments(); // safe: no second submission can resolve the same pending ask
  resolve("ok");
}
```

Apply this consistently across session rebuilds, UI binds, request/response handlers, and subprocess orchestration: define ownership, validate after awaits, prevent duplicate side effects, and clean up on settle.