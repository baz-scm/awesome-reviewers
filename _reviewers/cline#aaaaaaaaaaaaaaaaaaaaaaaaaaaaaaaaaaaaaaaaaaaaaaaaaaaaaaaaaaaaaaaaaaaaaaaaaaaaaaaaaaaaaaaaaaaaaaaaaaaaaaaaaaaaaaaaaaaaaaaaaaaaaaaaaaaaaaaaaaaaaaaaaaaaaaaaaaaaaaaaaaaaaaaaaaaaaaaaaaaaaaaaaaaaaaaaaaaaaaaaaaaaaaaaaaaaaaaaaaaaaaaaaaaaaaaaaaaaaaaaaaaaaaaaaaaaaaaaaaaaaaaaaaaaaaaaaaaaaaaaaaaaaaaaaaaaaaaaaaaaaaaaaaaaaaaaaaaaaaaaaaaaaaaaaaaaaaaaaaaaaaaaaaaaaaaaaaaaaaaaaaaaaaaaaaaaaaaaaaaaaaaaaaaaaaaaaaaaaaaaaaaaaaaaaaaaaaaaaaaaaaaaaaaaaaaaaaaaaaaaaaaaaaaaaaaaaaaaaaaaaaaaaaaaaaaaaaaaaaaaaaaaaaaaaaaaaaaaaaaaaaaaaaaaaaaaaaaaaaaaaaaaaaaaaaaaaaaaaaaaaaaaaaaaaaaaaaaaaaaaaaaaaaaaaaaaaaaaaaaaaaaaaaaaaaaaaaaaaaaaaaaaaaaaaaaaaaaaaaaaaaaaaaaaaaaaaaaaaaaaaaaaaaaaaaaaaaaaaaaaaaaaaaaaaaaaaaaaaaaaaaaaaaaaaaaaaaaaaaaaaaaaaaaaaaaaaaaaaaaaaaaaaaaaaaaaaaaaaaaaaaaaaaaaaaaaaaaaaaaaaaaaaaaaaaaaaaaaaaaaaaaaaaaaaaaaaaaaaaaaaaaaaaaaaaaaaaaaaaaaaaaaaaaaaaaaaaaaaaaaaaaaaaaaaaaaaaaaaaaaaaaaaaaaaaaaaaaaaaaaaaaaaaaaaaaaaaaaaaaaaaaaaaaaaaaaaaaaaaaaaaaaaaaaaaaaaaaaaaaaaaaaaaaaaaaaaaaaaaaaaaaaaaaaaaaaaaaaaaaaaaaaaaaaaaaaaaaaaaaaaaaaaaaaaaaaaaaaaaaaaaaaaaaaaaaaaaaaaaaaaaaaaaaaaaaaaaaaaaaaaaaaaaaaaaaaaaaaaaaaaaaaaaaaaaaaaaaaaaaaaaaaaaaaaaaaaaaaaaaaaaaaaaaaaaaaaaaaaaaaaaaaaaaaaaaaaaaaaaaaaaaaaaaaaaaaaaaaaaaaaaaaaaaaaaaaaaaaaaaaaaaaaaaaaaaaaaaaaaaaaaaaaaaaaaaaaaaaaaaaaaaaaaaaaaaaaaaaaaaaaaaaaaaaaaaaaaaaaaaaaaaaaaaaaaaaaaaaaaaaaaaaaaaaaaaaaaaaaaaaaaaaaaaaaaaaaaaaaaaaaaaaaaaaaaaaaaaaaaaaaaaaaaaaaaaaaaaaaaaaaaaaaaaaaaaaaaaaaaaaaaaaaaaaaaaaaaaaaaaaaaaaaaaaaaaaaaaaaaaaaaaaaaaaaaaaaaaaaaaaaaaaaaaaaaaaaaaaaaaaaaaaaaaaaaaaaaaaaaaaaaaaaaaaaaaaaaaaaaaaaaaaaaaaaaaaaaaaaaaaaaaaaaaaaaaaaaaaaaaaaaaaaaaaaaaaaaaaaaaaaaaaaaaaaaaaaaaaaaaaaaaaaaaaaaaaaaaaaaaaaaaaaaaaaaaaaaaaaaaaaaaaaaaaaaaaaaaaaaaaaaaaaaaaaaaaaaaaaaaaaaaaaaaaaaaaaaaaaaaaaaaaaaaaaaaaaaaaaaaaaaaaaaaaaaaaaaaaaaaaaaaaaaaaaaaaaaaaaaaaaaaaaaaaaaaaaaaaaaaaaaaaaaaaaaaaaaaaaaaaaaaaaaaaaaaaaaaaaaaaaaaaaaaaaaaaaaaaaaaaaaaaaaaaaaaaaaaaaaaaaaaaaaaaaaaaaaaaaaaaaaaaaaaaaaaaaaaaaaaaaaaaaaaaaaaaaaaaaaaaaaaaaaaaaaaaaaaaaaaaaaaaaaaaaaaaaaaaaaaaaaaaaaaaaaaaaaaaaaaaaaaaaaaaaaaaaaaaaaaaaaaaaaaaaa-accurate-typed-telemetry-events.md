---
title: Accurate, typed telemetry events
description: 'Telemetry and metrics must be trustworthy, not just present. Follow
  these rules when adding or changing instrumentation:


  1. **Use the typed catalog, never raw strings.** Register events in the shared catalog
  (e.g. `CORE_TELEMETRY_EVENTS`) and emit them through a dedicated typed `captureX`
  helper, not an inline literal like `telemetry.capture({ event:...'
repository: cline/cline#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
label: Observability
language: TypeScript
comments_count: 16
repository_stars: 70967
---

Telemetry and metrics must be trustworthy, not just present. Follow these rules when adding or changing instrumentation:

1. **Use the typed catalog, never raw strings.** Register events in the shared catalog (e.g. `CORE_TELEMETRY_EVENTS`) and emit them through a dedicated typed `captureX` helper, not an inline literal like `telemetry.capture({ event: "foo.bar", ... })`. This keeps names consistent, lets a catalog-consistency test catch drift, and ensures opt-out/sampling logic is applied uniformly.
2. **Make the data match reality.** A failure reason, stage, or identifier must reflect the actual condition being reported — don't report `TIMEOUT` for an empty-output case, or a generic ask failure as a `HANG`, and don't rename a property (e.g. `taskId` → `ulid`) without auditing and updating every call site, since positional args compile fine even when wrong.
3. **Instrument once, at the single source of truth.** Before adding a capture call, check whether the action is already recorded centrally (e.g. a runtime event pipeline); duplicating it elsewhere causes double-counting.
4. **Guarantee complete lifecycles.** For multi-phase operations (`started` → `succeeded`/`failed`/`retried`), every `started` must have a terminal event on *all* exit paths, including thrown errors and aborts — close out telemetry in `catch`/`finally` before rethrowing.
5. **Keep telemetry observational, not decisional.** Instrumentation should report what happened (e.g., "compaction and retry ran") rather than re-implementing success/failure judgments that another component (like the run loop) already owns — duplicated decision logic drifts out of sync over time.
6. **Justify new events before merging.** State concretely how the event will be used (a dashboard, an investigation query, a tripwire alert) and keep the event's cost and value explicit; this keeps the catalog lean and avoids "ship and hope" events that nobody queries.
7. **Track real progress signals.** When adding activity/heartbeat-style telemetry (e.g., run-idle detection), ensure all forms of legitimate activity (including streamed deltas) are counted, or the signal will produce false positives.

Example of the preferred pattern instead of an inline literal:
```ts
// core-events.ts
export function captureSdkStreamRetry(
  telemetry: ITelemetryService | undefined,
  properties: { attempt: number; delayMs: number; providerId: string },
): void {
  emit(telemetry, CORE_TELEMETRY_EVENTS.SDK.STREAM_RETRY, properties);
}

// call site
captureSdkStreamRetry(context.telemetry, { attempt, delayMs, providerId });
```