---
title: Accurate typed telemetry
description: 'Telemetry is only useful if it is both discoverable and trustworthy,
  so every new signal must satisfy two rules.


  1. **Go through the typed catalog, never a raw literal.** Register the event in
  the shared catalog (e.g. `CORE_TELEMETRY_EVENTS`) and add a typed `captureX`/`recordX`
  helper that encodes its exact shape. Ad-hoc `telemetry?.capture({ event:...'
repository: cline/cline#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
label: Observability
language: TypeScript
comments_count: 14
repository_stars: 70965
---

Telemetry is only useful if it is both discoverable and trustworthy, so every new signal must satisfy two rules.

1. **Go through the typed catalog, never a raw literal.** Register the event in the shared catalog (e.g. `CORE_TELEMETRY_EVENTS`) and add a typed `captureX`/`recordX` helper that encodes its exact shape. Ad-hoc `telemetry?.capture({ event: "my.event", ... })` calls bypass the one place events are documented and tested, and quietly drift from the catalog's conventions (naming, fields, PII rules — e.g. never the raw prompt/output text).

2. **Make the signal match reality, end-to-end.** Before adding or shipping a metric:
   - State up front how it will be consumed (dashboard, investigation query, or tripwire) — instrumentation added "just in case" tends to go unused or get misread.
   - Pick the reason/stage/outcome value that matches the actual condition observed, not a nearby or convenient one (e.g. don't report `TIMEOUT` for an empty-output path, or classify every `ask()` rejection as a `STREAM_TIMEOUT` hang) — mismatched reasons make the metric worse than having none.
   - Record the outcome on every exit path — success, thrown error, abort, and retry — so a `started` phase always gets a terminal `failed`/`succeeded` phase; a path that silently skips the terminal capture makes the metric overreport success.
   - Close out terminal spans/observations with the error *before* the underlying lifecycle or span ends (e.g. mark an LLM call's generation span failed in the same callback that sees the error, not in a later `onEnd`/consumer callback that fires after the span already closed).
   - Keep telemetry purely observational where a decision is already owned elsewhere (e.g. a run loop decides whether a turn is accepted); don't duplicate that classification logic inside the telemetry path, since the two copies will drift — instead, emit the raw fact (what ran, what it finished with) and let the consumer correlate it with the authoritative outcome.

Example of the failure mode to avoid:
```ts
// Bad: generic catch reports a specific reason that doesn't match the condition
catch {
  telemetryService.captureTerminalHang(TerminalHangStage.STREAM_TIMEOUT) // fires for ANY ask() failure
}

// Good: only emit the specific reason when the condition actually occurred
catch (error) {
  if (isStreamTimeout(error)) {
    telemetryService.captureTerminalHang(TerminalHangStage.STREAM_TIMEOUT)
  } else {
    telemetryService.captureTerminalHang(TerminalHangStage.ASK_FAILED)
  }
}
```