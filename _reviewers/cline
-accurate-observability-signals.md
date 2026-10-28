---
title: Accurate observability signals
description: 'Telemetry, metrics, and traces are only useful if they faithfully describe
  what actually happened, so treat observability data with the same rigor as business
  logic:'
repository: "cline/cline\r\n"
label: Observability
language: TypeScript
comments_count: 17
repository_stars: 70946
---

Telemetry, metrics, and traces are only useful if they faithfully describe what actually happened, so treat observability data with the same rigor as business logic:

1. Classify events by the real condition, not a convenient catch-all. If a `catch` or fallback branch can be reached by multiple distinct causes, give each cause its own reason/stage (e.g. don't report an "empty output" case as `TIMEOUT`, or any failed `ask()` rejection as `STREAM_TIMEOUT`); otherwise the resulting metric is uninterpretable.
2. Never let instrumentation imply a false outcome. Only mark an operation as succeeded/recovered when it actually met the success criteria (e.g. a retried turn only counts as "succeeded" if it finished cleanly with `stop`/`tool-calls`, not merely because it ran). When in doubt, keep the telemetry phase purely observational (e.g. `retried` with the observed finish reason) and let the single authoritative code path (the run loop, the main business decision) render the verdict — don't duplicate that judgment in the telemetry layer, since duplicated rules drift.
3. Capture terminal status before the underlying lifecycle closes. If a span, trace, or health record needs an error attached, record it at the point of failure, not later in an `onEnd`/finally callback after the resource has already been finalized — a late update cannot retroactively mark a closed span/generation.
4. Make failure/success capture resilient to its own side effects: if emitting a status notice or notifying a listener can throw, wrap it so a throwing listener still results in a terminal "failed" telemetry record (with a distinguishing `eventType` like `notice_threw`/`aborted`) rather than silently skipping the terminal event or leaking the wrong state forward (e.g. clear per-turn fields like `lastFinishReason` so a stale value from a prior turn isn't reported against a later failure).
5. Ensure instrumentation covers every code path that constitutes "progress" or "activity" for a health/liveness check — a streaming sub-event (e.g. tool-argument deltas) that never updates the last-activity timestamp will trigger false idle/hang alerts.
6. Attribute metrics to the correct unit of identity (session, generation, environment variable, launcher) and don't let one unit's failure or stamp bleed into another's — an existing identity stamp should win over a later one, and failure counts/health for a reloaded plugin generation must not be blamed on, or hidden behind, a different generation.
7. Only count telemetry for genuine user actions; internal plumbing calls (e.g. a CLI subcommand invoked by another client process) must not inflate activation/usage metrics.
8. Register first-party events through the project's central event catalog and typed capture helpers instead of raw literal strings, and cover new entries with the catalog-consistency test, so names, payload shape, and opt-out/export behavior stay uniform across the codebase.

```ts
// Bad: generic reason hides the real cause, and success is declared early
telemetryService.captureTerminalHang(TerminalHangStage.STREAM_TIMEOUT); // any ask() failure
this.captureTaskLifecycle(EVENT, { phase: "succeeded" }); // before checking retry.finishReason

// Good: reason matches the condition, success requires the real outcome
telemetryService.captureTerminalOutputFailure(TerminalOutputFailureReason.NO_OUTPUT);
const succeeded = retry.finishReason === "stop" || retry.finishReason === "tool-calls";
this.captureTaskLifecycle(EVENT, { phase: succeeded ? "succeeded" : "failed" });
```