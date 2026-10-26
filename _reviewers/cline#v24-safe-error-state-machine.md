---
title: Safe Error State Machine
description: 'Adopt an explicit “error-to-state” discipline: (1) classify errors precisely
  (especially retryability/timeouts), (2) never let async/cleanup failures leak as
  unhandled rejections or uncaught exceptions, and (3) ensure your UI/action state
  is consistent with the real side-effect boundary so retries/resends can’t duplicate
  work.'
repository: cline/cline#v24
label: Error Handling
language: TypeScript
comments_count: 10
repository_stars: 70891
---

Adopt an explicit “error-to-state” discipline: (1) classify errors precisely (especially retryability/timeouts), (2) never let async/cleanup failures leak as unhandled rejections or uncaught exceptions, and (3) ensure your UI/action state is consistent with the real side-effect boundary so retries/resends can’t duplicate work.

Actionable rules:
1) Precise retry eligibility
- Encode retry rules with table-driven tests and keep “unknown” cases non-retryable.
- Do not grant whole-turn retries just because a timeout occurred; preserve existing phase/budget/“silent provider” semantics.

2) Never leak async failures (fire-and-forget)
- Every promise created in a non-awaited/cleanup path must be caught (or intentionally rethrown into a handled path).
- For subprocess/worker streams, attach error listeners (e.g., stdin EPIPE) so errors don’t escape as uncaught exceptions.

3) Protect side-effect boundaries
- When an action can be dispatched and then fail, you must record/emit a “dispatch occurred” boundary; only those failures should offer resend.
- If a resend UI can reissue the same prompt, ensure the state machine distinguishes pre-dispatch vs post-dispatch outcomes.

4) Make error attribution stable
- Don’t let later callbacks or retries inherit stale “reason/phase” from previous steps. Reset/record attribution only at the real operation boundaries.

Code examples (patterns):

A) Catch attached/cleanup errors to avoid unhandled rejections
```ts
// BAD: detached rejection becomes unhandled
doThingAsync().then(() => updateUiSuccess());

// GOOD: keep old behavior stable + log
doThingAsync()
  .then(() => updateUiSuccess())
  .catch((e) => {
    console.error("Checkpoint commit failed", e);
    // optionally emit telemetry; keep UI consistent
  });
```

B) Absorb stdin stream EPIPE on child/server failures
```ts
child.stdin?.on("error", (err) => {
  // Record/annotate, but do not crash the host process.
  logger.debug(`stdin write failed: ${err.message}`);
});
```

C) Retryability: don’t blanket-allow timeouts
```ts
function isRetryable(error: unknown, phase: string): boolean {
  // Example: timeout is only retryable under explicit rules
  if (phase === "stream_part" || phase === "stream_callback") return false;
  if (isTimeoutReason(error)) return isTimeoutEligible(error); // NOT true by default
  return isRetryableBeyondBudget(error); // preserve prior semantics
}
```

D) Prevent duplicate resend with a dispatch boundary
```ts
// Model: record dispatch = true only once hub/controller confirms it.
if (dispatchConfirmed) {
  // post-dispatch failures => no resend of the same prompt
  uiState = { kind: "unconfirmed" }; // if it truly might still be pending
} else {
  // pre-dispatch failures => safe resend
  uiState = { kind: "unqueued" };
}
```

By enforcing these rules, you eliminate the common class of bugs seen across the discussions: silent state drift, duplicated side effects, leaked async exceptions, and incorrect retry/diagnostic decisions.