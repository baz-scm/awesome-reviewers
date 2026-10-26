---
title: Bounded Recovery & Safe Errors
description: 'When adding recovery/retry paths, require three invariants: (1) the
  failure is classified correctly, (2) recovery is bounded and safe (no silent behavioral
  changes), and (3) every async failure is routed to the owning error channel (no
  unhandled rejections, no stale timers), preserving side effects and accurate user/telemetry
  outcomes.'
repository: cline/cline#v1
label: Error Handling
language: TypeScript
comments_count: 11
repository_stars: 70862
---

When adding recovery/retry paths, require three invariants: (1) the failure is classified correctly, (2) recovery is bounded and safe (no silent behavioral changes), and (3) every async failure is routed to the owning error channel (no unhandled rejections, no stale timers), preserving side effects and accurate user/telemetry outcomes.

Practical rules:
- No silent fallback that changes semantics: if a takeover/replay can’t be proven safe, fail clearly and record structured telemetry (e.g., “owner gone” without transferring) rather than “best candidate” selection.
- Don’t broaden retries by error type alone: timeouts/cancellations are not automatically proof of a transient provider failure; keep existing retry budgets/guards and use dedicated “timeout phases”/limits.
- Preserve completed side effects during recovery: if a retry would repeat provider/tool side effects, either don’t retry, or replay only the safe parts and keep the completed activity in history.
- Route errors from async code paths:
  - Avoid detached `promise.then(async () => ...)` without a `.catch()` (or awaiting inside the existing try/catch).
  - Ensure event-driven failures (stdin/write/EPIPE, socket close, stream attach exceptions) are absorbed and turned into the same failure path that reports exit/error.
  - Cancel/clear observation timers and pending timers on spawn/attach failure so you don’t report false durations.
- Confirm what you settle: for control-plane or persistent state, only “drop/confirm” after server acknowledgment; otherwise retry later.

Example (safe recovery wrapper for “retry once if session lost”, preserving cancellation semantics):

```ts
async function withSessionRecovery<T>(
  operation: (client: Client) => Promise<T>,
  ctx?: { signal?: AbortSignal },
): Promise<T> {
  const client = await ensureConnectedClient();
  try {
    return await operation(client);
  } catch (err) {
    if (!isSessionLost(err)) throw err;
    if (ctx?.signal?.aborted) throw err; // cancelled calls must not be replayed

    const recovered = await recoverSession(client); // bounded: new handshake + single replay
    try {
      return await operation(recovered);
    } catch (retryErr) {
      throw retryErr; // let existing error handling decide how to surface
    }
  }
}
```

Example (fix unhandled checkpoint/recovery promise):

```ts
await say('checkpoint_created');
this.checkpointTracker.commit()
  .then((hash) => updateMessageWithHash(hash))
  .catch((e) => {
    // match prior behavior: log/telemetry, but do not create a fake success
    logCheckpointFailure(e);
  });
```

Apply this checklist to every new error/retry/recovery change in the category: ensure correctness (no silent semantic shifts), boundedness, preserved side effects, and deterministic error routing.