---
title: Accurate catalogued telemetry events
description: 'Every telemetry/tracing signal must be trustworthy end-to-end: typed,
  correctly labeled, and lifecycle-complete.


  1. Register, don''t hardcode. New events belong in the shared catalog (e.g. `CORE_TELEMETRY_EVENTS`)
  with a typed capture helper (e.g. `captureSdkStreamRetry`), not a raw string literal
  scattered in call sites. Add a catalog-consistency test....'
repository: cline/cline#`sleep 4`
label: Observability
language: TypeScript
comments_count: 15
repository_stars: 70979
---

Every telemetry/tracing signal must be trustworthy end-to-end: typed, correctly labeled, and lifecycle-complete.

1. Register, don't hardcode. New events belong in the shared catalog (e.g. `CORE_TELEMETRY_EVENTS`) with a typed capture helper (e.g. `captureSdkStreamRetry`), not a raw string literal scattered in call sites. Add a catalog-consistency test. Sandboxed/example-plugin code reporting through a host-provided telemetry bridge is the only exception, since its events are renamed/prefixed by the host and never match a first-party catalog entry.

2. Label the real condition. A reason/stage/outcome property must match what actually happened, not the nearest existing enum value. Don't report an empty-output condition as `TIMEOUT`, or any `ask` rejection as `STREAM_TIMEOUT` — add the missing enum value instead of overloading an existing one. Likewise, clear or scope per-turn/per-call state (e.g. `lastFinishReason`) so a stale value from a prior turn is never attributed to a later failure.

3. Close every lifecycle you open. If you emit a `started` phase, every code path out of that operation (success, caught error, rethrow, aborted retry, throwing listener) must emit a matching terminal phase (`succeeded`/`failed`) before the function returns or throws. For tracing, attach the error to the specific span whose operation actually failed *before* that span's lifecycle closes — don't rely on marking a still-open parent span after the fact. For metrics like usage/cost/first-token-latency, accumulate them so they survive a failed stream, a mid-stream throw, or a deadline race, rather than losing them when the happy path doesn't complete.

4. Observe, don't duplicate the verdict. Telemetry should report facts about what ran (e.g. "compaction + retry executed, retry finished with reason X"), not re-implement success/failure or abort classification that the main control flow already owns — duplicated judgment logic drifts and can contradict the real outcome. Name phases to reflect this (e.g. `retried`, not `completed`, when the telemetry itself makes no success claim).

5. Justify new signals. Before adding an event, state how it will be consumed (dashboard, incident investigation, tripwire) and keep its payload closed-set and narrowly scoped; document known coverage gaps explicitly rather than silently instrumenting only part of a path (e.g. note that a tracing integration doesn't cover a particular call type instead of wiring it to a resolver with nothing to attach to).

Example of a compliant addition:
```ts
// catalog
export const CORE_TELEMETRY_EVENTS = {
  TASK: { MAX_TOKENS_RECOVERY: TASK_MAX_TOKENS_RECOVERY_EVENT, ... },
};

// typed helper, closed-set properties, terminal phase always recorded
function captureMaxTokensRecovery(phase: "started" | "succeeded" | "failed" | "retried", eventType?: string) {
  telemetry.capture({ event: CORE_TELEMETRY_EVENTS.TASK.MAX_TOKENS_RECOVERY, properties: { phase, eventType } });
}
```
