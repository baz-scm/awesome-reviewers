---
title: Accurate telemetry lifecycle
description: 'Telemetry and tracing signals are only useful if they are precise, complete,
  and truthful about what actually happened. When adding or modifying observability
  instrumentation:'
repository: cline/cline#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
label: Observability
language: TypeScript
comments_count: 14
repository_stars: 70965
---

Telemetry and tracing signals are only useful if they are precise, complete, and truthful about what actually happened. When adding or modifying observability instrumentation:

1. Define events centrally and typed. Add new events/helpers to the shared telemetry registry (e.g. `CORE_TELEMETRY_EVENTS` + a typed `captureX` helper) instead of emitting raw string events ad hoc; this keeps event shapes discoverable, testable, and consistent across packages.

2. Instrument once, at the authoritative point. If usage/progress is already captured centrally (e.g. a runtime event pipeline), don't add a second capture call in a specific handler — that double-counts. Likewise, count all forms of real activity (e.g. streaming tool-call deltas), not just discrete lifecycle events, or health/idle signals will misfire.

3. Make lifecycle events complete and non-contradictory. Any `started` phase must always be paired with a terminal `succeeded`/`failed` phase, including on throw, abort, or listener-error paths — never leave a dangling "started" with no resolution. The recorded outcome must mirror the real downstream decision: don't mark an operation "succeeded" from an intermediate step if a later stage (e.g. the run loop) can still reject it. When in doubt, record what happened as a neutral, observational fact (e.g. `retried` with the resulting finish reason) rather than asserting a verdict that duplicates—and can contradict—logic owned elsewhere.

4. Classify failures by their actual cause. Reason/stage codes (e.g. `TIMEOUT`, `STREAM_TIMEOUT`) must match the specific condition observed; a catch-all `except` block or an "empty output" case must not be lumped into an unrelated reason, or the resulting metric becomes useless for diagnosis.

5. Attribute errors to the correct, still-open span/observation before it closes, so trace-level error status isn't lost once a generation/step has already ended.

6. Justify new events with a concrete use case — a dashboard query, an investigation workflow, or an alerting tripwire — and scope capture (sampling, event volume, which call sites count) deliberately; avoid counting internal/plumbing invocations as user-facing activations.

Example of a complete, non-contradictory lifecycle capture:
```ts
this.captureLifecycle(EVENT, { phase: "started" });
try {
  const result = await doRecoveryAttempt();
  const succeeded = loopAcceptsTurn(result); // mirror the real decision, don't re-derive it
  this.captureLifecycle(EVENT, { phase: succeeded ? "succeeded" : "failed" });
} catch (error) {
  this.captureLifecycle(EVENT, {
    phase: "failed",
    eventType: isAbortError(error) ? "aborted" : "threw",
  });
  throw error;
}
```