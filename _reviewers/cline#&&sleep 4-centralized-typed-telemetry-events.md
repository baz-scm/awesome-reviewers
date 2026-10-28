---
title: Centralized typed telemetry events
description: 'Every telemetry event must be declared once in the shared catalog (e.g.
  `CORE_TELEMETRY_EVENTS`) as a named constant, with a typed `captureX` helper that
  builds its properties — never call `telemetry.capture({ event: "some.raw.string",
  ... })` directly from feature code. This keeps event names discoverable and consistent,
  lets a catalog-consistency test...'
repository: cline/cline#&&sleep 4
label: Observability
language: TypeScript
comments_count: 7
repository_stars: 70980
---

Every telemetry event must be declared once in the shared catalog (e.g. `CORE_TELEMETRY_EVENTS`) as a named constant, with a typed `captureX` helper that builds its properties — never call `telemetry.capture({ event: "some.raw.string", ... })` directly from feature code. This keeps event names discoverable and consistent, lets a catalog-consistency test catch drift, and avoids leaking sensitive payloads (e.g. never include raw prompt text, only ids/counts/reasons). When adding a new event, also justify why it earns its keep: name the question it answers, the investigation it unblocks, or the tripwire it trips, and keep its payload a closed, bounded set of values rather than open-ended data.

The same discipline applies to the values inside an event: a failure reason, stage, or outcome field must match the condition actually observed, not the nearest existing enum value. If an "empty output" case is reported as `TIMEOUT`, or any ask failure is folded into a `STREAM_TIMEOUT` hang, the resulting metric silently conflates distinct failures and becomes unusable for triage — add a new enum value (e.g. `NO_OUTPUT`, `ASK_FAILED`) instead of reusing an unrelated one. Likewise, derive the data a telemetry call reports (e.g. "what ended this run") from the actual terminal event/outcome rather than incidental state like the last transcript entry, which may not correspond to the failure being recorded.

Example:
```ts
// Bad: raw string, scattered properties, wrong reason
telemetry.capture({ event: "sdk.stream_retry", properties: { attempt, delayMs } });
telemetryService.captureTerminalOutputFailure(TerminalOutputFailureReason.TIMEOUT); // actually no-output, not a timeout

// Good: catalog constant + typed helper + accurate reason
captureSdkStreamRetry(telemetry, { attempt, delayMs, providerId, modelId });
telemetryService.captureTerminalOutputFailure(TerminalOutputFailureReason.NO_OUTPUT);
```