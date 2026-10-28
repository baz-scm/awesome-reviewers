---
title: Typed, accurate telemetry
description: 'Telemetry and tracing instrumentation must be both structurally consistent
  and semantically truthful.


  Structure: never capture an event with a raw string literal scattered in application
  code. Register every event/counter name in the central catalog (e.g. `CORE_TELEMETRY_EVENTS`)
  and expose a typed `captureX`/`recordX` helper that fixes the property shape...'
repository: cline/cline#;sleep 4;
label: Observability
language: TypeScript
comments_count: 13
repository_stars: 70976
---

Telemetry and tracing instrumentation must be both structurally consistent and semantically truthful.

Structure: never capture an event with a raw string literal scattered in application code. Register every event/counter name in the central catalog (e.g. `CORE_TELEMETRY_EVENTS`) and expose a typed `captureX`/`recordX` helper that fixes the property shape (and scrubs anything sensitive, like prompt text). Call sites import only the helper, never build the event payload inline:

```ts
// bad
context.telemetry?.capture({ event: "sdk.stream_retry", properties: { attempt, delayMs } });

// good
captureSdkStreamRetry(context.telemetry, { attempt, delayMs });
```

This keeps event names, property keys, and property types (e.g. `ulid` vs `taskId`) identical across every call site, and makes "which events exist" discoverable and testable from one place.

Accuracy: an event is only useful if it reflects what actually happened.
- Classify failures by their real cause, not by the surrounding try/catch — a generic ask failure is not the same as a timeout; don't lump them under one stage/reason just because they're caught in the same block.
- Keep every lifecycle event paired: a `started` phase must always get a matching terminal phase (`succeeded`/`failed`/`completed`), including on throw, abort, or a listener error — never leave a started-but-never-closed record.
- Judge success by the same criteria the surrounding logic uses to accept the result; don't mark an operation "succeeded" in telemetry if the caller/loop still treats it as a failure (or vice versa). When in doubt, record the observed fact (e.g. finish reason, error type) rather than asserting a verdict the surrounding code doesn't actually make.
- Instrument once, at the central/shared pipeline, instead of adding a second capture call downstream — duplicate instrumentation double-counts usage.
- Only count an event toward a metric if it genuinely represents what the metric claims (e.g. don't count internal plumbing calls as user-initiated activations).

Before adding a new event, state briefly how it will be used (dashboard, investigation query, or tripwire) and keep its property set a closed, bounded vocabulary.