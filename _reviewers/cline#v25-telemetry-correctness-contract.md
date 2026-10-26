---
title: Telemetry correctness contract
description: 'All observability code must follow a “correctness & timing” contract:
  emit only when the signal is real, scoped to the correct unit of work, labeled with
  the true cause, and recorded before related tracing spans finalize—without affecting
  core behavior or identity.'
repository: cline/cline#v25
label: Observability
language: TypeScript
comments_count: 14
repository_stars: 70891
---

All observability code must follow a “correctness & timing” contract: emit only when the signal is real, scoped to the correct unit of work, labeled with the true cause, and recorded before related tracing spans finalize—without affecting core behavior or identity.

Apply these rules:
- **No stale attribution:** reset/clear per-turn/per-attempt fields at the start of the unit that owns them (avoid carrying previous causes into later failures).
- **Reason-faithful metrics:** the event “reason” (e.g., timeout/hang/abort) must match the actual failure mode; don’t lump unrelated errors into a single stage.
- **Lifecycle ordering:** if an error can arrive after a tracing lifecycle closes, ensure the terminal model/generation observation receives the error before span closure.
- **Close recovery telemetry:** every `started` telemetry phase must end with a terminal `succeeded`/`failed` phase, and “success” should be based on clean outcomes (not merely “no exception thrown somewhere”).
- **Cleanup timers/sampling windows:** cancel/disable observation timers on early failures to avoid false samples.
- **Resilience & opt-in:** never throw from telemetry paths; respect opt-outs; ensure telemetry adapters can’t interrupt inference.
- **Typed events, scoped catalogs:** use shared typed helpers / canonical event names; if you’re sandboxed and host-renamed (plugins), don’t force first-party core catalog rules that won’t match the final emitted name.
- **No identity/config mutation:** telemetry wiring must not alter bootstrap truth (session ids, restart/new classification). Keep telemetry state separate from core inference inputs.

Example pattern (accurate, scoped attribution):
```ts
// Clear per-turn attribution at the beginning of generation (not per-run)
this.state.lastFinishReason = undefined;

try {
  // ... open stream / run model
} catch (error) {
  // Record telemetry with the true scoped cause only
  // (don’t inherit previous turn’s finish reason)
  this.captureTurnFailure({ error, finishReason: this.state.lastFinishReason });
  throw error;
}
```

Example pattern (recovery telemetry terminal closure):
```ts
this.captureTaskLifecycle(EVENT, { phase: 'started' });
try {
  const retry = await retryOnce();
  const succeeded = retry.finishReason === 'stop' || retry.finishReason === 'tool-calls';
  this.captureTaskLifecycle(EVENT, { phase: succeeded ? 'succeeded' : 'failed' });
} catch (e) {
  this.captureTaskLifecycle(EVENT, { phase: 'failed', eventType: 'retry_threw' });
  throw e;
}
```