---
title: Error Boundaries And Retries
description: 'Define and enforce strict error-handling boundaries for async execution,
  streaming/subprocess I/O, and retry/recovery logic.


  **Standards**

  1) **No unhandled promise rejections at async boundaries**'
repository: cline/cline#v3
label: Error Handling
language: TypeScript
comments_count: 8
repository_stars: 70863
---

Define and enforce strict error-handling boundaries for async execution, streaming/subprocess I/O, and retry/recovery logic.

**Standards**
1) **No unhandled promise rejections at async boundaries**
- Never rely on detached promises for work that can fail; always attach a `.catch(...)` (or route through an awaited flow).
- If a function returns a promise and you attach a handler that can throw (e.g., inside `attach()`), ensure the promise chain catches *both* rejection and thrown exceptions.

2) **Preserve the truth of failures**
- Don’t “coerce” unrelated errors into benign outcomes (e.g., treat only real missing-objects as missing; surface other failures).
- Don’t claim success in UI/logic if the underlying operation can still fail asynchronously.

3) **Classify retryability correctly**
- Timeouts are not automatically evidence that a provider failure is transient; keep existing retry/budget semantics and diagnostics.
- Preserve timeout/abort attribution even when upstream stringifies reasons.
- Only retry/recover when it is safe (avoid replaying completed side effects).

4) **Stream/subprocess safety: absorb stdin write failures & cancel timers**
- If a child/server exits or closes stdin while writes are pending, attach `stdin.on('error', ...)` to prevent uncaught host crashes; still record the real exit/failure.
- Cancel observation timers when spawn fails; never emit “ran for N seconds” telemetry for commands that never started.

**Code example (two common fixes)**
```ts
// 1) Avoid detached promises that can reject without being handled.
// BAD:
checkpointTracker.commit().then(() => say('checkpoint_created'));

// GOOD: keep the failure observable (log/telemetry) and don’t claim success blindly.
await say('checkpoint_created');
checkpointTracker.commit().catch((err) => {
  logger.error?.('checkpoint commit failed', { err });
  // optionally update the prior message to remove/mark the hash
});

// 2) Catch exceptions thrown inside attach() during spawn.
// BAD:
spawnPromise.then(attach); // throws in attach => unhandled

// GOOD:
spawnPromise.then(attach).catch((error) => {
  handle.fail(new Error(`Couldn't keep this command inside your project: ${String(error)}`));
});
```

Apply these rules anywhere you: (a) detach async work, (b) bridge child-process/stdin/stdout streams, (c) implement recovery/retry policies, or (d) map low-level failures into user-facing outcomes.