---
title: Deterministic Error Handling
description: 'Adopt a single error-handling discipline across the codebase:


  1) Handle every async failure path

  - Never leave detached promises unhandled (always attach `.catch(...)` or route
  through a controlled async handler).'
repository: cline/cline#v30
label: Error Handling
language: TypeScript
comments_count: 12
repository_stars: 70894
---

Adopt a single error-handling discipline across the codebase:

1) Handle every async failure path
- Never leave detached promises unhandled (always attach `.catch(...)` or route through a controlled async handler).
- Ensure any stream/subprocess async errors are absorbed (attach `error` listeners) or converted into your existing failure reporting.
- Cancel observation/fallback timers when the underlying operation fails early.

2) Classify errors explicitly; don’t widen retry budgets
- Retry eligibility must be phase-aware (e.g., stream_part vs whole-turn, timeout vs provider retryability) and covered by table-driven tests.
- Avoid blanket rules like “timeouts are always retryable”; preserve existing “budget exhausted / stream-phase” logic.

3) Make side effects idempotent across retries/restarts
- Before publishing external effects (git pushes, orchestration steps), re-validate preconditions and repository/session state.
- Use durable or versioned state so retries after crashes don’t duplicate work; rollback transient state on failure.

4) Fail explicitly on capability disconnects; degrade without data loss
- When the component that owns a capability disconnects/detaches, fail with a user-safe message and track telemetry—don’t silently transfer/replay.
- On storage/reporting failures, preserve user value (e.g., keep truncated output, don’t drop full results; don’t replace history with incorrect “success”).

Code pattern (common fixes)
```ts
// (a) Never leave detached work as an unhandled promise
void checkpointTracker.commit().then((hash) => {
  if (hash) updateLastCheckpointHash(hash);
}).catch((error) => {
  logger.warn('checkpoint commit failed', { error });
});

// (b) Always clear timers on early failure
let fallbackTimer: NodeJS.Timeout | undefined;
try {
  fallbackTimer = setTimeout(() => settleAsFallback(), 1000);
  await doWork();
  clearTimeout(fallbackTimer);
  fallbackTimer = undefined;
  settleSuccess();
} catch (error) {
  if (fallbackTimer) clearTimeout(fallbackTimer);
  reportFailure(error);
}

// (c) Don’t blanket-retry timeouts; classify by phase
function isRetryable(error: unknown): boolean {
  if (isTimeout(error)) return false; // or only retry under proven safe conditions
  return isProviderRetryable(error);
}
```

If you standardize these four points (handled async, explicit retry classification, idempotent side effects, and safe degradation/UX messages), the failure scenarios discussed will consistently become bounded, debuggable, and user-correct.