---
title: Structured Error Handling Contracts
description: 'When code encounters failures, treat error handling as a contract: (1)
  capture every asynchronous exception, (2) classify error meaningfully for recovery/retry,
  and (3) ensure cleanup/telemetry never becomes misleading or breaks core behavior.'
repository: cline/cline#v8
label: Error Handling
language: TypeScript
comments_count: 9
repository_stars: 70867
---

When code encounters failures, treat error handling as a contract: (1) capture every asynchronous exception, (2) classify error meaningfully for recovery/retry, and (3) ensure cleanup/telemetry never becomes misleading or breaks core behavior.

Apply these rules:
1) Capture all async failures (no unhandled rejections)
- Any Promise chain that can both reject and throw must handle both in the same path.
- Detached Promises must be caught (or awaited) so failures don’t become unhandled.

Example pattern:
```ts
// Bad: throws inside attach() can become an unhandled rejection.
spawnPromise.then(attach, onError);

// Good: both rejection and attach() throws route through one handler.
spawnPromise
  .then(attach)
  .catch((err) => {
    // route to fail()/emit error state/logging
    handle.fail(new Error(`Spawn/attach failed: ${String(err)}`));
  });

// Detached promise must be caught.
void doWork().catch((e) => {
  logger.error('doWork failed', e);
});
```
2) Classify retryability precisely (timeouts ≠ always transient)
- Don’t blanket-mark timeouts (or other phases) as safe for whole-turn retries.
- Keep existing “safe retry windows” and guard against repeating side effects.
- When retrying, ensure you don’t bypass safety checks designed to prevent duplicate actions.

Standard: define an error classifier that returns categories like {retryableByWholeTurn, retryableByRequest, terminal} and use it consistently.
3) Preserve diagnostic truth; avoid unconditional fallbacks
- Only fall back when you’ve identified the correct failure class (e.g., missing prerequisite). Otherwise preserve the original error for the user and telemetry.
- Prefer “report exact failure” + “fallback only when prerequisite matches” over “try everything.”

4) Never let telemetry/sampling break inference or mislead users
- Wrap telemetry emissions so unexpected telemetry errors cannot abort inference or core work.
- For time-based observations, always cancel timers on failure paths (e.g., spawn failure) to avoid false “it ran for N seconds” samples.

5) Invariant breaks should fail explicitly
- If a postcondition is required (e.g., “artifacts must exist after ensureSessionPersisted”), avoid fallthrough into other flows. Prefer throwing a clear, user-actionable error or returning a safe refusal state.

Net effect: failures become predictable, retries become safe, metrics stay honest, and the system degrades gracefully without leaking unhandled async errors.