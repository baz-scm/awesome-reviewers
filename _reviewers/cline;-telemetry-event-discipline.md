---
title: Telemetry event discipline
description: 'Treat telemetry/observability events as a typed, centrally-owned contract,
  not ad-hoc strings. Apply these rules whenever you add or change an event:

  '
repository: cline/cline;
label: Observability
language: TypeScript
comments_count: 13
repository_stars: 70964
---

Treat telemetry/observability events as a typed, centrally-owned contract, not ad-hoc strings. Apply these rules whenever you add or change an event:

1. **Use the catalog, not literals.** Register new events as typed constants (e.g. `CORE_TELEMETRY_EVENTS.SESSION.PENDING_PROMPTS_DISCARDED`) with a typed `captureX` helper, and cover the registration with a catalog-consistency test. Never add a raw `telemetry.capture({ event: "some.string" })` literal for new events.
2. **Keep property names and call sites in sync.** Because capture helpers are often called positionally, renaming a parameter (e.g. `taskId` → `ulid`) silently corrupts data at every un-updated call site without a compiler error. When renaming a telemetry property, grep and update every call site in the same change, and prefer keeping the property name tied to what the value actually is.
3. **Make the reported condition match the real condition.** Don't reuse a generic reason/stage (e.g. `TIMEOUT`, `STREAM_TIMEOUT`) for an unrelated case (empty output, a generic ask failure) just because it's convenient — add a specific reason/stage so the metric isn't polluted and stays actionable for its intended question.
4. **Pair every "started" phase with a terminal phase.** For multi-step/lifecycle telemetry (started → succeeded/failed), ensure every code path out of the operation — including throws, aborts, and errors from downstream listeners — emits a matching terminal event before propagating, so dashboards never show an orphaned "started" with no resolution.
5. **Report observed facts, not duplicated verdicts.** Telemetry should describe what happened (e.g. "retried", "compaction ran") rather than re-implementing success/failure judgment that another component (e.g. the run loop) already owns; duplicating that logic in two places invites drift when one side changes. Similarly, avoid double-counting by routing instrumentation through the single existing central pipeline instead of adding a second capture call for the same action.
6. **Justify new events with a concrete use.** Before adding an event, state how it will be consumed (dashboard, investigation query, or tripwire) and keep its payload minimal (no sensitive content, closed set of values) — if nothing ends up reading it, remove it.

Example of a correctly registered, accurately-classified, paired event:
```ts
this.captureTaskLifecycle(TASK_MAX_TOKENS_RECOVERY_EVENT, { phase: "started" });
try {
  // ... operation ...
  this.captureTaskLifecycle(TASK_MAX_TOKENS_RECOVERY_EVENT, {
    phase: "retried",
    eventType: retry.finishReason, // fact, not a verdict
  });
} catch (error) {
  this.captureTaskLifecycle(TASK_MAX_TOKENS_RECOVERY_EVENT, {
    phase: "failed",
    eventType: this.isAbortError(error) ? "aborted" : "retry_threw",
  });
  throw error;
}
```