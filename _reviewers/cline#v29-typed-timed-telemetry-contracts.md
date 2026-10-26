---
title: Typed, Timed Telemetry Contracts
description: 'When adding or changing observability/telemetry, treat telemetry as
  a *contract*:


  1) **Use typed event helpers + catalog constants**

  - Prefer centrally-defined event IDs (constants) and typed `captureX` helpers over
  ad-hoc string literals.'
repository: cline/cline#v29
label: Observability
language: TypeScript
comments_count: 11
repository_stars: 70893
---

When adding or changing observability/telemetry, treat telemetry as a *contract*:

1) **Use typed event helpers + catalog constants**
- Prefer centrally-defined event IDs (constants) and typed `captureX` helpers over ad-hoc string literals.
- Add tests that assert the emitted event constant/shape.

2) **Make telemetry semantically correct**
- Emit the *right* cause/reason (don’t label generic failures as timeouts).
- Attribute to the correct scope (e.g., per-turn reset of `finishReason`; avoid stale attribution across turns/retries).
- Preserve required error details for specific failure classes (don’t drop provider details when wrapping errors).

3) **Emit at the right lifecycle time**
- If telemetry is mirrored into tracing/OTel (Langfuse/OTel spans), ensure terminal error data is recorded **before** the integration/span lifecycle closes; late reporting can leave generation spans UNSET.

4) **Keep telemetry safe and non-breaking**
- Respect opt-out, sanitize/redact payloads, and ensure telemetry capture paths never throw.

5) **Guard against refactors corrupting payloads**
- If you rename telemetry properties, update all call sites (positional args can silently compile and corrupt payloads). Consider tests that validate property keys/values.

Example pattern (typed, testable, lifecycle-safe):
```ts
// 1) Emit identity via typed helper/constants
import { CORE_TELEMETRY_EVENTS, captureSdkStreamRetry } from "...";

function onStreamError({ error, request, context, streamTelemetry }: any) {
  const retry = computeRetry(error);
  if (!retry) return;

  // 2) Semantically correct + scoped message
  context.telemetry?.capture({
    event: CORE_TELEMETRY_EVENTS.SDK.STREAM_RETRY,
    properties: captureSdkStreamRetry({
      providerId: request.providerId,
      modelId: request.modelId,
      attempt: retry.attempt,
      maxAttempts: retry.maxAttempts,
      delayMs: retry.delayMs,
      error_type: getErrorType(error),
    }),
  });
}

// 3) Lifecycle-safe: record before end/close if tracing integration ends early
async function recordBeforeSpanCloses(telemetryLifecycle: any, recordError: (e: unknown)=>Promise<void>, err: unknown) {
  telemetryLifecycle.onLanguageModelCallEnd = async () => {
    await recordError(err); // do not wait for a later onError that may be too late
  };
}
```

Adopt this checklist for every telemetry change to avoid silent contract drift, misattributed causes, and missing trace-level error visibility.