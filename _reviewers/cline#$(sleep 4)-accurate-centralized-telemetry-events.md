---
title: Accurate, centralized telemetry events
description: Telemetry and metrics are only useful if they are structurally consistent
  and semantically correct, so both properties must be enforced for every new event.
repository: cline/cline#$(sleep 4)
label: Observability
language: TypeScript
comments_count: 13
repository_stars: 70978
---

Telemetry and metrics are only useful if they are structurally consistent and semantically correct, so both properties must be enforced for every new event.

1. Centralize event names and shapes. Never emit a raw string event/property (e.g. `"sdk.stream_retry"`, `"desktop.marketplace.install"`) from first-party code. Add the event to the shared catalog (e.g. `CORE_TELEMETRY_EVENTS`) and expose a typed `captureX` helper that callers use, with a catalog-consistency test asserting the constant exists. Before wiring a new helper into an existing pipeline, check whether the condition it reports is already captured centrally downstream (e.g. generic tool-usage capture) to avoid double-counting the same action from two call sites.

2. Make the reported value match the real condition. A rename of a parameter (e.g. `taskId` → `ulid`) must update every call site, not just compile; an event fired from a broad `catch` or generic "no output" branch must carry a reason that actually distinguishes that case (timeout vs. empty output vs. ask-failure), not a reason copy-pasted from a nearby branch. Diagnostic fields must be derived from the actual terminal state/response of the operation being reported, not from a stale value left over from an earlier turn or an unrelated transcript entry — reset or recompute per-attempt state so a previous run's finish reason, error, or diagnostic can never leak into the current report.

3. Treat lifecycle/phase events as a contract: every `started` must be paired with exactly one terminal `succeeded`/`failed` (or equivalent), including on throw, abort, or listener-failure paths. Only count an outcome as successful once the operation has actually completed cleanly end-to-end (capture the outcome after, not before, any side effect such as a notice that could itself fail); otherwise the metric overreports success. When a sub-step is purely observational (e.g. "a retry ran with outcome X") and a higher-level process still makes the final accept/reject decision, don't have the sub-step also emit its own success/failure verdict — that duplicates and can contradict the authoritative outcome.

Example of a correctly scoped, typed capture:
```ts
// shared/telemetry.ts
export const TASK_MAX_TOKENS_RECOVERY_EVENT = "task.max_tokens_recovery";

// core-events.ts
export const CORE_TELEMETRY_EVENTS = {
  TASK: { MAX_TOKENS_RECOVERY: TASK_MAX_TOKENS_RECOVERY_EVENT, /* ... */ },
};

// call site
this.captureTaskLifecycle(TASK_MAX_TOKENS_RECOVERY_EVENT, { phase: "started" });
try {
  const retry = await attemptRecovery();
  this.captureTaskLifecycle(TASK_MAX_TOKENS_RECOVERY_EVENT, {
    phase: "retried",
    eventType: retry.finishReason, // observed fact, not a verdict
  });
} catch (error) {
  this.captureTaskLifecycle(TASK_MAX_TOKENS_RECOVERY_EVENT, {
    phase: "failed",
    eventType: this.isAbortError(error) ? "aborted" : "recovery_threw",
  });
  throw error;
}
```
Before adding a new event, also state briefly how it will be consumed (dashboard, investigation query, or tripwire) and keep its payload closed-set and bounded — this keeps the catalog from accumulating events nobody can act on.