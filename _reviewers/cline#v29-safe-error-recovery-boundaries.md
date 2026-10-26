---
title: Safe Error Recovery Boundaries
description: 'Treat error handling as a lifecycle contract: capture the *exact* failure
  stage, ensure cleanup/timeout logic can’t lie, and only retry/replay work when it’s
  proven safe.'
repository: cline/cline#v29
label: Error Handling
language: TypeScript
comments_count: 12
repository_stars: 70893
---

Treat error handling as a lifecycle contract: capture the *exact* failure stage, ensure cleanup/timeout logic can’t lie, and only retry/replay work when it’s proven safe.

**Standards**
1) **Cover all failure paths in async chains**
- Use `.then(...).catch(...)` (or `try/catch`) so exceptions thrown inside `attach`/callbacks are handled, not turned into unhandled rejections.
- Never fire-and-forget promises for important error outcomes (checkpoints, background commits, checkpoint hashes).

2) **Cancel timers / pending observations on early failure**
- If you arm an observation timer before stdin writes/spawn, cancel it when spawn/start fails; otherwise you’ll emit false “ran for X ms” samples.

3) **Never transition state on unconfirmed dispatch**
- When UI/offers retry, rely on an explicit “dispatch confirmed” signal (or typed failure that says “pre-dispatch” vs “post-dispatch”).
- Don’t offer resend for failures that happened after the hub already dispatched (double-send risk).

4) **Retry/replay only with explicit safety gates**
- Don’t blanket-classify timeouts as whole-turn retryable; respect retry budgets and “might have been processed” semantics.
- For session lost/re-handshake, detect the error across transports and replay only once, and only when the client was actually responsible for that session.

5) **Ensure asynchronous subprocess/stream errors can’t escape uncaught**
- If stdin piping can throw (EPIPE/EOF on Windows), attach `stdin.on('error', ...)` (or convert to a controlled failure) so the host doesn’t crash.

6) **Make recovery settlement conditional on control-plane confirmation**
- Keep retry queues/batches until you have confirmation of success (e.g., only delete journal entries after a confirmed DELETE).

**Pattern examples**

```ts
// 1) Cover both rejected promises and synchronous throws in the same flow
void loadMxc()
  .then((mxc) => mxc.spawn(/* ... */))
  .then((sandboxed) => {
    // If attach() throws, this catch must still run.
    handle.attach(sandboxed);
  })
  .catch((err) => {
    const reason = err instanceof Error ? err.message : String(err);
    handle.fail(new Error(`Couldn't keep command in sandbox: ${reason}`));
  });

// 2) Cancel observation timers on early failures
let timer: NodeJS.Timeout | undefined;
try {
  timer = setTimeout(() => reportOnce({ exited: false }), observationMs);
  timer.unref?.();
  await spawn();
  // ... later
  clearTimeout(timer);
} catch (e) {
  if (timer) clearTimeout(timer); // prevents false sample
  throw e;
}

// 3) Gate resend/retry on confirmed dispatch boundary
if (sendFailure.dispatched === true) {
  // Don't offer resend; work may already have been processed.
  surfaceAsUnconfirmedOrRetryableOnlyAfterSessionRecovers();
} else {
  // Pre-dispatch failure: safe to resend (or offer resend).
  offerResendDraft();
}
```

Adopt this as a coding standard for orchestration, streaming transports, subprocess/sandbox executors, and persistence/recovery loops: your code should never (a) leave unhandled async failures, (b) emit misleading timing/health signals, or (c) trigger duplicate work based on uncertain stage knowledge.