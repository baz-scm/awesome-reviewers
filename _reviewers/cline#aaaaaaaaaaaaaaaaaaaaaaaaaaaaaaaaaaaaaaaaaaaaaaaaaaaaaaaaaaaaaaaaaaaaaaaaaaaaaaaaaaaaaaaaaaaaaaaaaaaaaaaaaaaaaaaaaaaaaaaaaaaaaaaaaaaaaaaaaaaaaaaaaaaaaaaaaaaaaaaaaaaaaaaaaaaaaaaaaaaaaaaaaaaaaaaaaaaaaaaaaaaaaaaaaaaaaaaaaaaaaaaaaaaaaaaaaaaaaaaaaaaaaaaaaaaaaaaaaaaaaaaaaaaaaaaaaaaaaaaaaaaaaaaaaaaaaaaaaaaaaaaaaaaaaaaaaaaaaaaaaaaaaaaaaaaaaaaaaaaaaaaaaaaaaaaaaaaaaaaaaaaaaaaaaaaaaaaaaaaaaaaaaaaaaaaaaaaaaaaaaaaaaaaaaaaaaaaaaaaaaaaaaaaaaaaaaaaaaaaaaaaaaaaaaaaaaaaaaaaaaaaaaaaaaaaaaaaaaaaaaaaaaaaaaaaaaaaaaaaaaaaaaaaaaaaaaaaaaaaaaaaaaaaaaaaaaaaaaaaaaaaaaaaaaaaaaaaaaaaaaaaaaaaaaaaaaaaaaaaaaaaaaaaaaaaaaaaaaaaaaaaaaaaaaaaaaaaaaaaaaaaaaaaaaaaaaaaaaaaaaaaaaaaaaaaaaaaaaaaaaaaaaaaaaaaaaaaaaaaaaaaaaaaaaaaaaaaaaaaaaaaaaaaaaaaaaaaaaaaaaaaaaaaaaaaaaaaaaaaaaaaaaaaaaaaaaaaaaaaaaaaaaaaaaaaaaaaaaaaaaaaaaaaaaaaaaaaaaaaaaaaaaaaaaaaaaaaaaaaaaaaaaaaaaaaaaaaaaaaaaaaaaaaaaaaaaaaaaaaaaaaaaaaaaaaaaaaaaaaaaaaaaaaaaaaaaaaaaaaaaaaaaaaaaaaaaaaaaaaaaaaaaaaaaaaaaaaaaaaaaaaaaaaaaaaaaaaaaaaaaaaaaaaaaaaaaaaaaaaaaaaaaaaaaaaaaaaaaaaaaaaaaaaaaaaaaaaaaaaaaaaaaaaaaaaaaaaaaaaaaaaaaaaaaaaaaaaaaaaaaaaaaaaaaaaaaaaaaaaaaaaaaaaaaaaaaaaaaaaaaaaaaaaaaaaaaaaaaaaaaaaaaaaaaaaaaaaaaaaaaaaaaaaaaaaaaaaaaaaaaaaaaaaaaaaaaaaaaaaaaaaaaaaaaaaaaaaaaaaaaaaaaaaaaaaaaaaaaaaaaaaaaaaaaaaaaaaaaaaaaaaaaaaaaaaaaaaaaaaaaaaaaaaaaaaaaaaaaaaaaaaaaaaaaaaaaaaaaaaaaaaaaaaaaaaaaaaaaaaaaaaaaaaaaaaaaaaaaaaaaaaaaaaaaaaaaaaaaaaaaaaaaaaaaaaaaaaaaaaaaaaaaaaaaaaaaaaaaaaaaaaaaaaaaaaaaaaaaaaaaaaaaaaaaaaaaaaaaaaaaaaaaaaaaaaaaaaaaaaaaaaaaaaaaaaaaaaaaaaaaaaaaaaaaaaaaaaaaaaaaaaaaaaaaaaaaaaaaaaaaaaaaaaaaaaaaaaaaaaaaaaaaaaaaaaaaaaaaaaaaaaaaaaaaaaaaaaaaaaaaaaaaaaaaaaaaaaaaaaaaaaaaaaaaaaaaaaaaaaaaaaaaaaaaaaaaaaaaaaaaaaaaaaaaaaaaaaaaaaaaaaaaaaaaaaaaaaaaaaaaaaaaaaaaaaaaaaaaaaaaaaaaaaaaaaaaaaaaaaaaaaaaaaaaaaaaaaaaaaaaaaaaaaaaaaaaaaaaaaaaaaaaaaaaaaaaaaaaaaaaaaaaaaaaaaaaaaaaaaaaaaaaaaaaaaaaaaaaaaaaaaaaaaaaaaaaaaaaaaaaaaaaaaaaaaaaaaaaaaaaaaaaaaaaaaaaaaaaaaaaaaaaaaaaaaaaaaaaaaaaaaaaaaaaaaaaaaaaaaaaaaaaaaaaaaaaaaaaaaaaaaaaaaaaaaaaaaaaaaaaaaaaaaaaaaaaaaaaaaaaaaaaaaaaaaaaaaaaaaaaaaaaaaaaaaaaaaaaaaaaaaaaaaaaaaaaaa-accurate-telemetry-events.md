---
title: Accurate telemetry events
description: Telemetry and metrics are only useful if the data they carry is correct
  and complete, so treat emitting an event with the same rigor as production logic.
repository: cline/cline#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
label: Observability
language: TypeScript
comments_count: 10
repository_stars: 70973
---

Telemetry and metrics are only useful if the data they carry is correct and complete, so treat emitting an event with the same rigor as production logic.

- Register every first-party event in the shared catalog (e.g. `CORE_TELEMETRY_EVENTS`) with a typed capture helper instead of a raw string. This prevents name drift between emitter and dashboard, and gives refactors a compiler-checked call site.
- When renaming or restructuring an event's properties, audit every call site. Positional/duck-typed calls compile fine even when the semantics change, so a rename like `taskId` → `ulid` can silently mix two different ID formats under the same property key across events.
- Derive the captured value from the actual, current outcome, not from a convenient but possibly stale proxy. A catch-all `catch` block should not stamp every failure as a specific stage (e.g. `STREAM_TIMEOUT`) unless that's really what happened; a diagnostic should inspect the response/finish-reason that actually ended the current turn, not a transcript tail or a value carried over from a previous turn, and must clear per-turn state so a later failure doesn't inherit an earlier turn's cause.
- Give every "started" phase a matching terminal phase ("completed"/"failed"/"retried") on all exit paths, including thrown errors and aborts, so a lifecycle metric never has orphaned starts.
- Keep the event's semantics honest: it should report what was observed, not assert a verdict (success/failure) that belongs to the caller's own decision logic. Name phases to reflect what actually ran (e.g. `retried` rather than `completed`) so the event can't be misread as claiming an outcome it didn't judge.
- Before adding a new event, write down who will use it and how (dashboard, investigation query, or tripwire) and keep its property set to a bounded, closed vocabulary — this keeps volume and cost predictable and avoids events nobody can act on.

Example of a correctly paired lifecycle emission:
```ts
this.captureTaskLifecycle(TASK_MAX_TOKENS_RECOVERY_EVENT, { phase: "started" });
try {
  const retry = await this.generateAssistantMessage({ overflowRecovery: true });
  this.captureTaskLifecycle(TASK_MAX_TOKENS_RECOVERY_EVENT, {
    phase: "retried",
    eventType: retry.finishReason, // observed fact, not a verdict
  });
} catch (error) {
  this.captureTaskLifecycle(TASK_MAX_TOKENS_RECOVERY_EVENT, {
    phase: "failed",
    eventType: "recovery_threw",
  });
  throw error;
}
```