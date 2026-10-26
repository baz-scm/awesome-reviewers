---
title: Telemetry correctness and policy
description: All observability events must be emitted with a correct, stable, and
  timely contract—so that opt-out works, dashboards/joins don’t break, and tracing/metrics
  remain analyzable.
repository: cline/cline#v23
label: Observability
language: TypeScript
comments_count: 9
repository_stars: 70889
---

All observability events must be emitted with a correct, stable, and timely contract—so that opt-out works, dashboards/joins don’t break, and tracing/metrics remain analyzable.

Use this checklist for every new/changed telemetry capture:
1) **Go through approved telemetry helpers/adapters**
   - Use the project’s typed `core-events`/emit helpers (or the sandboxed plugin telemetry bridge) so opt-out is respected and policy tests can cover it.
   - Avoid bypassing helper layers that already implement opt-out/required-capture rules.

2) **Keep event names and property shapes stable**
   - If you rename an event property key (e.g., `taskId` → `ulid`), update *all* call sites and add/extend tests that assert the captured payload shape.

3) **Scope dimensions correctly (turn vs run)**
   - Reset/derive attributes per the intended granularity; e.g., don’t let a previous turn’s `finishReason` leak into a later turn’s failure telemetry.

4) **Make staged telemetry always reach a terminal state**
   - For `phase: started`, ensure a corresponding `phase: succeeded|failed` is captured even when hooks/listeners/notice emission throws.

5) **Record stream/tracing failures before spans close**
   - For streaming providers, ensure the error is attached to the relevant lifecycle observation before that generation/span is ended; late error reporting can leave generation-level spans with no exception.

6) **Use truthful, granular reason codes**
   - Don’t over-generalize different causes into one bucket; add explicit enum values (e.g., `NO_OUTPUT` vs `TIMEOUT`, `ASK_FAILED` vs `STREAM_TIMEOUT`) to avoid metric inflation and to keep diagnostics actionable.

Illustrative pattern (staged telemetry with correct terminal outcome):
```ts
// Pseudo-structure: started -> (succeeded | failed) always
this.captureTaskLifecycle(EVENT, { phase: "started" });
try {
  await emitNotice(); // may throw
  // outcome capture only after notice
  this.captureTaskLifecycle(EVENT, { phase: "succeeded" });
} catch (err) {
  this.captureTaskLifecycle(EVENT, {
    phase: "failed",
    eventType: isAbort(err) ? "aborted" : "notice_threw",
  });
  throw err;
}
```

Outcome: events remain queryable, opt-out-safe, analytically correct (no stale attribution), and trace/metric failures are visible at the right lifecycle moments.