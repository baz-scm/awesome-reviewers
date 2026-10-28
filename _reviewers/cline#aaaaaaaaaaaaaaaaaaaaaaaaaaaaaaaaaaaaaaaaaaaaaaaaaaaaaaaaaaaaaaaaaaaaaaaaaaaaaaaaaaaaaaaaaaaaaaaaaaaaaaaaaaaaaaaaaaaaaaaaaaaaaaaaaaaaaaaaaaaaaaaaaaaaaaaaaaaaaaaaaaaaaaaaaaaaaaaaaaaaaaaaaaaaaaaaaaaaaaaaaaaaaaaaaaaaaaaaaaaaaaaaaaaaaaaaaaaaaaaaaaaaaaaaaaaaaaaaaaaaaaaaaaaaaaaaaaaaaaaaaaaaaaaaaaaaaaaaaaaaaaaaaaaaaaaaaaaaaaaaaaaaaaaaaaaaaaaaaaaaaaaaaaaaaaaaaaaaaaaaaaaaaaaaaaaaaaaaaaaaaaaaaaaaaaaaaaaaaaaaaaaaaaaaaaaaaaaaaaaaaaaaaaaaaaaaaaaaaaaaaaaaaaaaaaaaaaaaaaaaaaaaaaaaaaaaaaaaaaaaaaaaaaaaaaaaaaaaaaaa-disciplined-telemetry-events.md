---
title: Disciplined telemetry events
description: Every telemetry event must be registered as a constant in the central
  catalog (e.g. `CORE_TELEMETRY_EVENTS`) with a typed `captureX` helper, instead of
  being captured with a raw string literal scattered through the codebase. Add a catalog-consistency
  test asserting the constant exists. This keeps event names, payload shapes, and
  PII rules (e.g. never...
repository: cline/cline#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
label: Observability
language: TypeScript
comments_count: 12
repository_stars: 70964
---

Every telemetry event must be registered as a constant in the central catalog (e.g. `CORE_TELEMETRY_EVENTS`) with a typed `captureX` helper, instead of being captured with a raw string literal scattered through the codebase. Add a catalog-consistency test asserting the constant exists. This keeps event names, payload shapes, and PII rules (e.g. never capturing raw prompt text) enforceable at compile time and in one discoverable place:

```ts
// Bad: raw string literal, untyped properties
telemetry.capture({ event: "sdk.stream_retry", properties: { attempt, delayMs } });

// Good: cataloged event + typed helper
export const CORE_TELEMETRY_EVENTS = {
  SDK: { STREAM_RETRY: SDK_STREAM_RETRY_TELEMETRY_EVENT },
};
export function captureSdkStreamRetry(
  telemetry: ITelemetryService | undefined,
  props: { attempt: number; delayMs: number; providerId: string },
) {
  telemetry?.capture({ event: CORE_TELEMETRY_EVENTS.SDK.STREAM_RETRY, properties: props });
}
```

Beyond registration, two correctness rules apply to any event or reason code:

1. **The reported reason/outcome must match the actual condition observed.** Don't reuse a generic reason (e.g. `TIMEOUT`, `STREAM_TIMEOUT`) for a different failure mode (empty output, a generic ask-error), and don't silently rename an identifier's semantics (e.g. swapping `taskId` for `ulid`) without updating every call site — positional-argument renames compile cleanly but corrupt the data. Add a distinct reason/stage value when the condition is genuinely different, and verify all call sites when a property's meaning changes.

2. **Every lifecycle event that reports a `started` phase must emit a matching terminal phase** (`succeeded`/`failed`/equivalent), including on throws, aborts, or listener/hook errors — never leave a started event dangling. The success/failure classification must mirror the actual, authoritative outcome of the operation (e.g. what the run loop ultimately accepts) rather than a local guess that could contradict it; when in doubt, make the event purely observational (what happened) rather than a verdict, and let downstream consumers join it with the real outcome.

Before adding a new event, confirm it answers a specific question or will drive a dashboard/alert/tripwire — avoid speculative events that nobody will read.