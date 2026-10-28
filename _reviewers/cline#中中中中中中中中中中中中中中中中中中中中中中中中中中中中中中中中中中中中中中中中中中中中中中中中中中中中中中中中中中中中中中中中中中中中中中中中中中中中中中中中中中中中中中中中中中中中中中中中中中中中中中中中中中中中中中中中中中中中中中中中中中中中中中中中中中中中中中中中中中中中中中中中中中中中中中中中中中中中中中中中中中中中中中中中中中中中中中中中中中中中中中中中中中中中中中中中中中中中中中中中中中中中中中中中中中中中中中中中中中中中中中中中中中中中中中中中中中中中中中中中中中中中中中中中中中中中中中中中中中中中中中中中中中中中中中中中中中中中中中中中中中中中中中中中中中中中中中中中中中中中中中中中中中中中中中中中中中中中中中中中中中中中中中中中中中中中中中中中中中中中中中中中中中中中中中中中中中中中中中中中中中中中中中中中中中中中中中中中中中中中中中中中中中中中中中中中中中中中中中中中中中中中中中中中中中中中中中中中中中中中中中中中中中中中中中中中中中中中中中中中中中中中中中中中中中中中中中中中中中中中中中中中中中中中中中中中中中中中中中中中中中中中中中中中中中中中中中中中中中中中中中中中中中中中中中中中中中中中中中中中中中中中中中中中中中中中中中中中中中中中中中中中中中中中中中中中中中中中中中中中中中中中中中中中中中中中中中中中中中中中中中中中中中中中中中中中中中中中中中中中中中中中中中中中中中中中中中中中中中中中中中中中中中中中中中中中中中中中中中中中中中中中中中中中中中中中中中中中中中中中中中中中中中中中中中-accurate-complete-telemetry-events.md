---
title: Accurate, complete telemetry events
description: 'Telemetry and metrics are only useful if they are precise, complete,
  and consistently defined — treat them with the same rigor as production code.


  1. **Use centralized, typed event definitions.** Don''t emit raw string event names/properties
  from feature code. Define the event (and a typed capture helper) once in the shared
  telemetry registry (e.g....'
repository: cline/cline#中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中
label: Observability
language: TypeScript
comments_count: 13
repository_stars: 70986
---

Telemetry and metrics are only useful if they are precise, complete, and consistently defined — treat them with the same rigor as production code.

1. **Use centralized, typed event definitions.** Don't emit raw string event names/properties from feature code. Define the event (and a typed capture helper) once in the shared telemetry registry (e.g. `CORE_TELEMETRY_EVENTS` / `core-events.ts`) and import it everywhere it's used, so names, shapes, and property keys can't drift between callers or packages.

2. **Make the reported reason match the actual condition.** A failure/stage enum value must reflect what really happened, not whatever was convenient. E.g. don't report `TIMEOUT` for an "empty output" condition, or classify every rejection from an `ask()` call as a `STREAM_TIMEOUT` hang — add a dedicated reason (`NO_OUTPUT`, `ASK_FAILED`, etc.) so the metric stays trustworthy. Likewise, when renaming a property (e.g. `taskId` → `ulid`), update every call site and verify the value's semantics actually match the new name — a positional rename that silently keeps passing the old value corrupts the data with no compiler error.

3. **Give every lifecycle event a guaranteed terminal state.** If you emit a `started` phase, every code path out of that operation — success, expected failure, thrown error, abort — must emit a matching terminal phase (`succeeded`/`failed`/`completed`) before propagating, or the metric will silently undercount failures:
```ts
this.captureLifecycle(EVENT, { phase: "started" });
try {
  const result = await doWork();
  this.captureLifecycle(EVENT, { phase: "succeeded" });
  return result;
} catch (error) {
  this.captureLifecycle(EVENT, { phase: "failed", eventType: classify(error) });
  throw error;
}
```
Keep this telemetry purely observational — record what happened, don't duplicate or contradict a judgment that other logic (e.g. a run loop) is responsible for making.

4. **Make liveness/progress signals account for all real activity.** If a heartbeat or idle-detection mechanism counts only some event types as "progress," any real but uncounted activity (e.g. streaming tool-call-delta chunks) can trigger false alarms. Audit what counts as progress and add coverage (tests spanning the timeout threshold) for activity that should suppress it.

5. **Justify new events with a concrete use.** Before adding a new metric/event, state how it will be consumed — dashboard, investigation query, or tripwire for a specific failure mode — and keep its value set closed and its emission bounded, so it doesn't become unused noise.