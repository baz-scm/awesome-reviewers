---
title: Telemetry event integrity
description: 'Telemetry is only useful if the data it produces can be trusted, so
  treat instrumentation with the same rigor as production logic:


  1. **Use the central typed catalog, not raw strings.** Register every first-party
  event in the shared catalog (e.g. `CORE_TELEMETRY_EVENTS`) with a typed `captureX`
  helper, instead of inlining literal event-name strings at the...'
repository: 'cline/cline

  '
label: Observability
language: TypeScript
comments_count: 13
repository_stars: 70942
---

Telemetry is only useful if the data it produces can be trusted, so treat instrumentation with the same rigor as production logic:

1. **Use the central typed catalog, not raw strings.** Register every first-party event in the shared catalog (e.g. `CORE_TELEMETRY_EVENTS`) with a typed `captureX` helper, instead of inlining literal event-name strings at the call site. This keeps event names, property shapes, and renamed fields consistent and lets a catalog-consistency test catch drift. When a property or helper signature changes (e.g. `taskId` → `ulid`), update every call site — a positional rename that compiles cleanly can silently ship the wrong value under the new key and break downstream joins.

2. **Make the reported reason/outcome match the actual condition.** Don't reuse a convenient-but-inaccurate classification (e.g. labeling an "empty output" case as `TIMEOUT`, or any `ask` failure as a `STREAM_TIMEOUT` hang) — add a dedicated reason/stage when the existing ones don't fit. A metric that conflates distinct failure modes is worse than no metric.

3. **Guarantee complete lifecycle pairing.** For multi-phase events (`started` → `succeeded`/`failed`), every `started` must have exactly one terminal emission on *every* exit path, including thrown errors, aborts, and listener/hook exceptions — emit the terminal capture before rethrowing or before a notice that could itself throw. Keep observational phases (e.g. "the retry ran") clearly separate from outcome judgments (e.g. "the run succeeded") so an intermediate stage can't misrepresent — or duplicate — the final result that downstream logic independently decides.

4. **Instrument once, at the right layer.** Before adding a new capture call, check whether the event is already emitted centrally (e.g. via a shared runtime/event-adapter pipeline); adding a second call site at a lower layer causes double counting.

5. **Justify new events before adding them.** Each new event should have a concrete, stated use (a dashboard, an investigation query, or a tripwire) and a bounded, well-understood cost (sampling, frequency, property set) — call this out explicitly in the PR description.

Example of the catalog pattern to follow:
```ts
// shared/src/services/telemetry.ts
export const TASK_MAX_TOKENS_RECOVERY_EVENT = "task.max_tokens_recovery";

// core/src/services/telemetry/core-events.ts
export const CORE_TELEMETRY_EVENTS = {
  TASK: { MAX_TOKENS_RECOVERY: TASK_MAX_TOKENS_RECOVERY_EVENT, /* ... */ },
};
export function captureTaskMaxTokensRecovery(
  telemetry: ITelemetryService | undefined,
  props: { phase: "started" | "succeeded" | "failed"; eventType?: string },
): void { /* typed capture */ }
```
Avoid:
```ts
telemetry.capture({ event: "task.max_tokens_recovery", properties: { phase: "started" } }); // raw string, untyped, no catalog entry
```