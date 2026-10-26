---
title: Serialize and Claim Async
description: 'For any async flow that can overlap (teardown vs idle, retries, replacements,
  concurrent sessions, plugin generations, subprocess fallbacks), require: (1) per-entity
  serialization for state mutations, (2) synchronous ownership/claim before awaiting,
  (3) attempt/generation-scoped validation in later callbacks, and (4) explicit timeout/cancellation
  plus...'
repository: cline/cline#v5
label: Concurrency
language: TypeScript
comments_count: 11
repository_stars: 70864
---

For any async flow that can overlap (teardown vs idle, retries, replacements, concurrent sessions, plugin generations, subprocess fallbacks), require: (1) per-entity serialization for state mutations, (2) synchronous ownership/claim before awaiting, (3) attempt/generation-scoped validation in later callbacks, and (4) explicit timeout/cancellation plus cleanup of resources created during the operation.

Practical checks:
- Serialize writes/mutations by a stable key (sessionId/taskId/plugin-generation). Use a per-key promise queue/chain so late completions can’t overwrite newer state.
- Claim ownership synchronously before the first `await` if a later action must not “steal” resolution (e.g., pending prompt/ask). Then deliver asynchronously, but only to the claimed attempt; reject/route replacements elsewhere.
- In every `then`/callback after `await`, validate that the work is still the current attempt (generation/owner/slot still matches). If not, exit without mutating state.
- Never allow indefinite waits: add capability-appropriate deadlines, propagate `AbortSignal`, and ensure promise settlement triggers cleanup (detach listeners, clear timers, drop inherited pipes).

Code pattern (claim-before-await + stale-guard):
```ts
// Claim synchronously.
const claimed = pendingAskResolve;
if (!claimed) return false;
const claimId = currentAttemptId();
pendingAskResolve = undefined; // or mark claimed

const hasAttachments = !!(images?.length || files?.length);
if (hasAttachments && deliverAttachments) {
  await deliverAttachments(() => currentAttemptId() === claimId);
}

// Validate before mutating any shared state.
if (currentAttemptId() !== claimId) return true;
setTurnPhase('streaming');
claimed(prompt ?? '');
return true;
```

If the operation can overlap, add these guards even if it “usually” doesn’t—tests should include teardown/retry/overlap scenarios (out-of-order completion, cancellation during backoff, replacement during delivery, and late callback after release/stop).