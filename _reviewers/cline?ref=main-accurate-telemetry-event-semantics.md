---
title: Accurate telemetry event semantics
description: 'Telemetry must describe what actually happened, not just something that
  happened nearby. Two failure patterns show up repeatedly:


  1. **Wrong classification/label.** A `catch` or condition block often covers several
  distinct failure modes, but emits a single hard-coded reason/stage/property that
  only matches one of them. For example, reporting every "no...'
repository: cline/cline?ref=main
label: Observability
language: TypeScript
comments_count: 10
repository_stars: 70980
---

Telemetry must describe what actually happened, not just something that happened nearby. Two failure patterns show up repeatedly:

1. **Wrong classification/label.** A `catch` or condition block often covers several distinct failure modes, but emits a single hard-coded reason/stage/property that only matches one of them. For example, reporting every "no output captured" case as `TIMEOUT`, tagging any failed `ask()` call as `STREAM_TIMEOUT`, or renaming a property (`taskId` → `ulid`) without updating call sites so the wrong value is sent under the new key. Before adding a reason code or property, verify the condition you're branching on actually matches the label you emit; if one handler covers multiple causes, add distinct reason values (e.g. `NO_OUTPUT` vs `TIMEOUT`, `ASK_FAILED` vs `STREAM_TIMEOUT`) and pick the one that's true.

2. **Incomplete or misleading lifecycle.** Multi-phase events (`started` → `succeeded`/`failed`) must always reach a terminal phase that reflects the real outcome — including when a listener throws, the operation is aborted, or an error occurs after the "success" path already began. Derive the terminal status from the authoritative outcome (e.g. what the run loop actually accepts, the current turn/response, the terminal span still open) rather than from stale state (e.g. the last transcript message, which may predate the response being judged) or from a local judgment call that can contradict the caller's eventual decision. When a sub-component's success/failure is really decided downstream, emit a factual, non-judgmental state (e.g. `retried` with the observed finish reason) instead of a verdict that can diverge from the real result.

Before shipping a new event, confirm you can state concretely how it will be consumed (dashboard, investigation query, or tripwire) — speculative events that duplicate existing instrumentation (e.g. re-counting tool usage already captured centrally) should be removed in favor of the single source of truth.

```ts
// Bad: same reason for two different conditions
catch {
  telemetryService.captureTerminalHang(TerminalHangStage.STREAM_TIMEOUT); // true for any ask() failure
}

// Good: classify by the actual condition
catch (error) {
  telemetryService.captureTerminalHang(
    isTimeout(error) ? TerminalHangStage.STREAM_TIMEOUT : TerminalHangStage.ASK_FAILED,
  );
}

// Bad: terminal phase can be skipped if emit() throws
this.captureTaskLifecycle(EVENT, { phase: "started" });
await this.emit({ ... }); // throws -> no "failed"/"succeeded" ever recorded

// Good: guarantee a terminal phase on every path
try {
  await this.emit({ ... });
} catch (error) {
  this.captureTaskLifecycle(EVENT, { phase: "failed", eventType: classify(error) });
  throw error;
}
```