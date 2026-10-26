---
title: Concurrency Ownership & Lifetimes
description: 'When async work spans multiple awaits (or can be retried), prevent races
  by making ownership/lifecycle *explicit* and monotonic:


  1) Claim before await'
repository: cline/cline#v9
label: Concurrency
language: TypeScript
comments_count: 8
repository_stars: 70868
---

When async work spans multiple awaits (or can be retried), prevent races by making ownership/lifecycle *explicit* and monotonic:

1) Claim before await
- If an async result can only be applied once (e.g., “resolve pending question”), synchronously “claim” the pending slot before awaiting attachment/delivery/prep.
- After the await, verify the same claim is still valid; otherwise route as follow-up or fail fast.

2) Gate by generation/lifecycle tokens
- For UI binds/unmounts or session replans, increment a generation (or use an attempt id) before detaching.
- Any async continuation must discard results when its generation no longer matches the current one.

3) Serialize overlapping writes/updates per key
- For persistence/state transitions that can overlap (status writes, queued polls, checkpoint commit metadata), chain/serialize per session/key so terminal states (cancelled/teardown) can’t be overwritten by late in-flight operations.

4) Target the right object immediately
- Don’t re-discover “the latest thing” in a later microtask/timer; capture the exact message/index/record that must be updated right after creation, then update that captured reference.

5) Add explicit timeouts/cancellation for responder-absent waits
- Any “wait forever” path should have capability-appropriate deadlines and cancellation/cleanup. If you intentionally keep indefinite waits, document the policy and ensure a separate watchdog exists.

6) Cleanup after settle
- Once an operation resolves/rejects (especially when using timeouts), remove listeners/timers/stdio pipes to prevent late events from mutating disposed state or keeping the process alive.

Example pattern (claim-before-await + generation gate):
```ts
let pendingResolve: ((text: string) => void) | undefined;
let generation = 0;

async function resolvePending(text: string, deliverAttachments?: () => Promise<void>) {
  const resolve = pendingResolve;
  if (!resolve) return false;

  // Claim synchronously
  pendingResolve = undefined;
  const myGen = generation;

  if (deliverAttachments) {
    try {
      await deliverAttachments();
      if (myGen !== generation) return true; // stale delivery: do not apply
    } catch {
      // If delivery fails, still fulfill with text (or the agreed fallback)
    }
  }

  // Apply exactly once
  resolve(text);
  return true;
}
```

Adopt these rules consistently: reviewers should ask “Who owns this async continuation?” and “What happens if a newer state arrives before awaits finish?”—then enforce claim, generation gating, and per-key serialization accordingly.