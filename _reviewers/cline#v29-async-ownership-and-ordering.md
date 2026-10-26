---
title: Async ownership and ordering
description: When async overlap is possible, make “who owns the next state” and “which
  result is allowed to write” explicit. Otherwise late completions will overwrite
  newer truth.
repository: cline/cline#v29
label: Concurrency
language: TypeScript
comments_count: 10
repository_stars: 70893
---

When async overlap is possible, make “who owns the next state” and “which result is allowed to write” explicit. Otherwise late completions will overwrite newer truth.

Apply these rules:
1) **Claim synchronously before `await`:** if a shared slot/question/task can be resolved by multiple concurrent submissions, capture/claim the resolver before any asynchronous delivery so a second submission can’t “steal” the same slot.
2) **Await the critical path that must survive teardown:** if a resource (UI push, disposal, runtime stop) can happen before downstream work finishes, either `await` it or tie teardown to completion of that specific operation.
3) **Guard every write with ownership metadata:** include a `sessionId`, `runId`, `generation`, or `attemptToken`, and only write when it still matches the current owner. Late writers must become no-ops.
4) **Serialize transitions under a lock/single-flight:** operations like rebuild/reopen/start/replace should run in a controlled order; coalescing must also invalidate superseded work.
5) **Make retries/delays abort-aware:** any `sleep`/backoff/poll loop should respect cancellation signals; do not “reattach” work after the caller has canceled.

Example pattern (claim-before-await + guarded completion):
```ts
// Shared slot for an outstanding question.
let pendingResolve: ((text?: string) => void) | undefined
let pendingAttempt = 0

async function resolvePending(
  text: string,
  deliverAttachments?: () => Promise<void>,
) {
  const resolve = pendingResolve
  const attempt = pendingAttempt
  if (!resolve) return false

  // Claim before any await.
  pendingResolve = undefined
  pendingAttempt += 1

  try {
    if (deliverAttachments) {
      await deliverAttachments()
    }

    // Guard: only the claimed attempt may complete the slot.
    if (attempt !== pendingAttempt - 1) return true
    resolve(text)
    return true
  } catch (e) {
    // Release only your own claim so retries remain possible.
    if (attempt === pendingAttempt - 1) {
      pendingResolve = resolve
    }
    return true
  }
}
```
In code reviews, ask: “What happens if a second action arrives before the first `await` finishes?” and “Can a late promise still write after disposal/rebuild/teardown?”