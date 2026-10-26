---
title: Accurate Telemetry Contracts
description: 'Telemetry must be *truthful, well-attributed, lifecycle-correct, and
  schema-consistent*—or it becomes harder to debug than having no data.


  Apply this standard:'
repository: cline/cline#v5
label: Observability
language: TypeScript
comments_count: 12
repository_stars: 70864
---

Telemetry must be *truthful, well-attributed, lifecycle-correct, and schema-consistent*—or it becomes harder to debug than having no data.

Apply this standard:
1) **Attribute with correct scope**: reset/derive “cause” fields per turn/span, not per run. Don’t let a previous turn’s finish reason leak into later failures.
2) **Emit the right reason/stage**: a metric/event value must match the actual condition (e.g., don’t label “empty output” as `TIMEOUT`; don’t label any ask failure as `STREAM_TIMEOUT`). If needed, add a dedicated reason/stage enum.
3) **Preserve accurate identifier schema**: when renaming telemetry properties, update all call sites (positional args won’t be caught by TS) so downstream joins use a stable key.
4) **Avoid double-counting**: understand the central instrumentation pipeline; don’t re-capture the same metric in secondary handlers.
5) **Respect tracing lifecycle ordering**: ensure stream/model-call errors are recorded before the relevant tracing/span observation closes; otherwise generation spans may remain `UNSET`.
6) **Lock behavior with focused tests**: add regression tests that assert exact emitted telemetry fields/enums and tracing span status/exception (including streaming and threshold/timing edge cases).
7) **No observability side-effects**: telemetry configuration/hooks must not mutate operational bootstrap truth (e.g., sessionId semantics), or event meaning changes.

Minimal example pattern (turn-scoped attribution + enum correctness):
```ts
// Reset per turn (not per run)
this.state.lastFinishReason = undefined;

// Only emit hang metrics for real timeouts
try {
  await this.ask("command_output", chunk);
} catch (e) {
  if (e instanceof StreamTimeoutError) {
    telemetry.captureTerminalHang(TerminalHangStage.STREAM_TIMEOUT);
  } else {
    telemetry.captureTerminalHang(TerminalHangStage.ASK_FAILED);
  }
  throw e;
}
```

If you can’t clearly map an emitted telemetry field/value to the exact underlying observed condition (with correct timing/lifecycle), add/adjust the instrumentation rather than emitting “closest” data.