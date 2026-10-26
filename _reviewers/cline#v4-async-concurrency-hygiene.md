---
title: Async Concurrency Hygiene
description: When async work can overlap, shared state must be updated and side effects
  must be authorized in a way that late/duplicate executions cannot overwrite newer
  state or leak resources.
repository: cline/cline#v4
label: Concurrency
language: TypeScript
comments_count: 7
repository_stars: 70864
---

When async work can overlap, shared state must be updated and side effects must be authorized in a way that late/duplicate executions cannot overwrite newer state or leak resources.

**Standard rules**
1. **Claim before awaiting** for any “single-consumer” resolution (pending prompts, tasks, turn decisions). Make the claim/invalidations happen synchronously *before* the first `await`.
2. **Guard with eligibility** (generation tokens / per-entity checks / “still current?” predicates) so late callbacks are ignored.
3. **Serialize per key** (sessionId/taskId/etc.) where out-of-order writes are harmful; otherwise chain operations on a per-key promise queue.
4. **Bind async continuations to the exact target computed now**. Avoid “re-find latest” after a delay/await if other operations can create newer targets.
5. **Propagate cancellation**: every sleep/backoff/retry/stream pump must accept the abort signal; check cancellation before starting the next attempt.
6. **Clean up on early settle**: if you resolve/reject before natural completion (fallback settle, timeout, race), remove listeners and close/drop inherited resources (pipes, streams, timers) so a background grandchild can’t keep the host alive.

**Example pattern (claim + generation + abort-aware sleep)**
```ts
let currentClaim: symbol | null = null;
let generation = 0;

export async function resolveOnce(params: {
  deliverAttachments?: () => Promise<void>;
  abortSignal: AbortSignal;
}): Promise<boolean> {
  const myGen = ++generation;
  const myClaim = Symbol('claim');
  // Claim synchronously so a second submission can’t resolve the same question.
  if (currentClaim) return false;
  currentClaim = myClaim;

  try {
    if (params.deliverAttachments) {
      // Abort-aware wait.
      await sleepWithAbort(50, params.abortSignal);
      if (myGen !== generation || currentClaim !== myClaim) return false;
      await params.deliverAttachments();
    }
    // Publish result only if still eligible.
    if (currentClaim !== myClaim) return false;
    currentClaim = null;
    return true;
  } catch {
    // Release only this claim.
    if (currentClaim === myClaim) currentClaim = null;
    throw;
  }
}

function sleepWithAbort(ms: number, signal: AbortSignal) {
  return new Promise<void>((resolve, reject) => {
    const t = setTimeout(resolve, ms);
    const onAbort = () => {
      clearTimeout(t);
      reject(new DOMException('Aborted', 'AbortError'));
    };
    if (signal.aborted) return onAbort();
    signal.addEventListener('abort', onAbort, { once: true });
  });
}
```

Applying this consistently prevents the concrete failures seen in these discussions: stale late writers overwriting newer teardown/status, polling or retries overwriting actions, out-of-order async commits updating the wrong target, duplicate/overlapping “resolve pending” operations, rebuild/supersession races, abort-insensitive backoff, and early-settle subprocess hangs due to leaked pipes/listeners.