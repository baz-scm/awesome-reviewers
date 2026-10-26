---
title: Accurate Telemetry Lifecycle
description: 'Treat telemetry as a correctness-sensitive contract: event names/properties
  must match the real observed state, be emitted at the right time in the tracing/lifecycle,
  and never distort other metrics or behavior.'
repository: cline/cline#v20
label: Observability
language: TypeScript
comments_count: 11
repository_stars: 70886
---

Treat telemetry as a correctness-sensitive contract: event names/properties must match the real observed state, be emitted at the right time in the tracing/lifecycle, and never distort other metrics or behavior.

Apply these rules:
1) **Respect telemetry contracts**
- Use the approved event catalog/constants for event names and properties (avoid ad-hoc raw strings that bypass rules).
- Avoid double-counting: if a pipeline already emits tool-usage/task telemetry, don’t emit the same signal again in downstream handlers.

2) **Classification must be truthful**
- Don’t map distinct failure modes to the same reason/stage. If you have both TIMEOUT and “no output,” add a distinct enum value (e.g., `NO_OUTPUT`) and emit it accordingly.
- Only record a specific hang stage when it’s actually that condition; otherwise create a dedicated “ask_failed/ask_error” stage or gate emission on the real cause.

3) **Lifecycle timing must be correct**
- Ensure terminal tracing/span observations receive the error before the lifecycle closes. If error reporting can arrive after spans end, plumb the pending error into the earlier lifecycle hook.
- Reset attribution per turn (finish reason, error details) to prevent stale values being inherited.
- If you emit a `started` telemetry phase, guarantee a terminal phase on every exit path (success, failure, rethrow), including listener throwing/catch blocks.

4) **Prevent false samples**
- Cancel observation timers on spawn/execution failures; otherwise you’ll record “exited:false” runtime samples that never actually ran.

5) **Telemetry must not mutate behavior**
- Telemetry configuration/wiring should attach hooks/observability only; it must not rewrite core bootstrap truth that affects session semantics (e.g., sessionId signaling).

Example pattern for lifecycle closure (TypeScript):
```ts
captureTaskLifecycle(EVENT, { phase: "started" });
try {
  // do work
  captureTaskLifecycle(EVENT, { phase: "succeeded" });
} catch (e) {
  captureTaskLifecycle(EVENT, { phase: "failed", eventType: "recovery_threw" });
  throw e;
}
```

Add/extend tests to lock these invariants:
- Assert the exact telemetry phases emitted on success/failure.
- Assert span status/exception at the correct generation-level granularity.
- Reproduce edge cases (stream retries, wrapped errors, empty-output vs timeout, spawn failures) so regressions can’t silently skew dashboards/decisions.