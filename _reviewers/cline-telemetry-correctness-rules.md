---
title: Telemetry correctness rules
description: 'Adopt a single standard for all observability code:


  1) Be policy-compliant and opt-out safe

  - Prefer typed helper functions for telemetry events (fixed event names and fixed
  payload shapes).'
repository: ClInE/cLiNe
label: Observability
language: TypeScript
comments_count: 17
repository_stars: 70838
---

Adopt a single standard for all observability code:

1) Be policy-compliant and opt-out safe
- Prefer typed helper functions for telemetry events (fixed event names and fixed payload shapes).
- Never rely on raw event strings outside the allowed scopes.
- Telemetry capture must be a no-op when the adapter/host telemetry is disabled, and must never throw.

2) Ensure attribution is correct (per-turn, per-retry)
- Reset attribution fields at the start of each turn (or at the correct lifecycle boundary) to prevent stale causes (e.g., finishReason) leaking into later failures.
- Classify failure reasons using dedicated dimensions so distinct causes aren’t conflated into one bucket.

3) Keep metrics specific and non-inflating
- Don’t emit a “timeout” (or similar) reason when the code path is “any ask failure”.
- Avoid double counting by using the central instrumentation pipeline only once.

4) Preserve trace/span lifecycle ordering
- For streaming/tracing, record errors/exception details before the relevant spans end; ensure generation spans receive the correct status/exception.

5) Avoid false samples in observations
- If you start an observation timer, cancel it on early failures (e.g., spawn/connect errors) so you don’t report synthetic “ran for N seconds” samples.

6) Keep observability from mutating core behavior
- Observability hooks must attach telemetry and instrumentation, but must not rewrite bootstrap identity/session inputs that core uses to decide resume vs new session.

Practical pattern (safe helper + fixed payload shape)
```ts
// telemetry helpers: fixed catalog event + fixed properties; never throws
export function capturePendingPromptsDiscarded(
  telemetry: ITelemetryService | undefined,
  details: { sessionId: string; count: number; reason: 'queue_abort' | 'session_teardown' },
): void {
  if (!telemetry?.isEnabled()) return;
  try {
    telemetry.capture({
      event: CORE_TELEMETRY_EVENTS.SESSION.PENDING_PROMPTS_DISCARDED,
      properties: { ...details },
    });
  } catch {
    // observability must not break execution
  }
}
```

Checklist for PRs touching observability
- [ ] Uses helper(s) with fixed event names and fixed payload shape.
- [ ] Respects opt-out and never throws.
- [ ] Attribution/reset is correct per turn/retry.
- [ ] Reason dimensions are specific (no conflation).
- [ ] No double counting (instrumentation is centralized).
- [ ] Trace/span error/status ordering is correct for streaming.
- [ ] Timers/censors are canceled on early failures.
- [ ] Telemetry code does not mutate session/core bootstrap identity inputs.
- [ ] Adds/updates tests for ordering/shape and opt-out behavior.