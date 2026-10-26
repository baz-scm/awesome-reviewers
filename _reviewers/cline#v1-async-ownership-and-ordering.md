---
title: Async ownership and ordering
description: 'When async work overlaps (retries, polling, teardown, concurrent requests),
  shared state must have an unambiguous owner and deterministic ordering. Apply these
  rules:'
repository: cline/cline#v1
label: Concurrency
language: TypeScript
comments_count: 14
repository_stars: 70862
---

When async work overlaps (retries, polling, teardown, concurrent requests), shared state must have an unambiguous owner and deterministic ordering. Apply these rules:

1) Claim ownership synchronously (before the first await)
- If two submissions could “resolve” the same pending operation, convert the ownership decision into an atomic/linear step.

```ts
// Bad: checks/pending read then awaits delivery
const resolve = pendingAskResolve
if (hasAttachments) await deliverAttachments()
resolve(answer)

// Good: claim first, then await delivery
const resolve = pendingAskResolve
pendingAskResolve = undefined // claim now
const hasAttachments = !!(images?.length || files?.length)
if (hasAttachments && deliverAttachments) {
  await deliverAttachments(() => /* optional current check */ true)
  // don’t allow a second submission to resolve the same question
}
resolve(answer)
```

2) Capture the exact target before await; don’t re-search later
- If you need to update “the checkpoint_created message you just emitted”, store its index/id immediately after creation. Never rely on a later lookup that may observe newer messages.

3) Serialize side effects per entity (per session/file/request)
- For shared persistence, state transitions, or rate-limited calls: chain operations per key (sessionId, filePath, session). Avoid “two writes overlap; last one wins unintentionally”.

4) Use generation tokens / live “isCurrent” semantics
- For queued work + cancellation/replacement: every async callback must be able to tell whether it’s still current (generation counter) and must not re-activate after a newer request.

5) Make cancellation/deadlines abort-aware and close late completions
- Backoff sleeps and retries must be interruptible.
- If a deadline fires while a connection/start is still in-flight, ensure the late resolver cleans up (e.g., disconnect) instead of leaving resources or changing state after failure.

6) Add explicit timeouts for “owner gone” / “no one can answer” waits
- Never allow an await that has no timeout when the responder might never arrive.

These practices prevent the common failure modes shown across the discussions: stale/wrong state overwrites, attachments or follow-ups lost to ownership races, out-of-order persistence updates, hung/indefinite waits, and late completions that outlive their cancellation/deadline.