---
title: Concurrency Ownership and Ordering
description: 'When async work touches shared or persisted state, treat concurrency
  as “ownership + ordering + lifecycle”: claim the right to complete work synchronously,
  serialize the final commit per entity, and refuse to apply stale results.'
repository: cline/cline#v16
label: Concurrency
language: TypeScript
comments_count: 14
repository_stars: 70882
---

When async work touches shared or persisted state, treat concurrency as “ownership + ordering + lifecycle”: claim the right to complete work synchronously, serialize the final commit per entity, and refuse to apply stale results.

Use these rules in review:
1) Claim ownership before any await
- If multiple submissions/retries can target the same pending item, atomically “claim” it, then do any async work.

```ts
async function resolvePending(pending: { fn: Function | undefined }, deliverAttachments?: () => Promise<void>) {
  const resolve = pending.fn;
  if (!resolve) return false;
  pending.fn = undefined; // claim now

  const hadAttachments = !!deliverAttachments;
  if (hadAttachments) {
    await deliverAttachments!(); // second submit can no longer resolve the same item
    // core/host echo policy can be handled separately
  }

  resolve(/* prompt */);
  return true;
}
```

2) Serialize or guard commit side effects per key
- If teardown/dispose or stop can overlap with in-flight updates, ensure the terminal/teardown write lands last and intermediate writers can’t overwrite it.
- Practical: chain writes per session/entity (promise queue) and add guards that trigger when the write actually begins.

3) Use generation/scope tokens to drop stale callbacks
- Attach a monotonically increasing “generation/attempt id” to the async operation; before committing, verify the operation is still current for that session/scope.

4) Cancellation checks at attempt/tool boundaries
- Don’t assume cancellation propagates automatically. Check `signal.aborted` (or equivalent) before starting the next attempt/batch boundary, and ensure retries don’t leak/attach detached work.

5) Background/non-blocking work must target the correct entity captured at creation time
- If you intentionally don’t await a commit, do not “re-find” the target later by scanning shared arrays; capture the exact index/id at creation time and update that exact target in the background.

6) Listener/timer/pipe cleanup is part of concurrency correctness
- Register event handlers once (no stacking on retries), and ensure late settling doesn’t leave open listeners/pipes that keep processes alive.
- When aborting or timing out, remove handlers and cancel streams so the system reaches a consistent end state.

If any async code can: (a) run concurrently with teardown/stop/reload, (b) update persisted/shared state, or (c) be retried, then review it through this checklist—ownership claim, per-key ordering/serialization, generation gating, explicit cancellation, correct target capture, and cleanup.