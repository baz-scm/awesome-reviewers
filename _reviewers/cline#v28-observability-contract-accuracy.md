---
title: Observability Contract Accuracy
description: 'Observability changes must be treated like correctness-critical logic:
  emit telemetry with accurate attribution and lifecycle timing, via typed event contracts,
  and lock behavior with regression tests.'
repository: cline/cline#v28
label: Observability
language: TypeScript
comments_count: 10
repository_stars: 70892
---

Observability changes must be treated like correctness-critical logic: emit telemetry with accurate attribution and lifecycle timing, via typed event contracts, and lock behavior with regression tests.

Guidelines:
- **Attribute to the correct unit**: per-turn fields (e.g., finish reason/model failure) must be reset/cleared so later failures don’t inherit earlier causes.
- **Emit at the right lifecycle time**: if traces/OTel observations close in a lifecycle callback, don’t report the error after the span is already finalized. Prefer reporting the pending terminal error before the observation closes.
- **Cover streaming/retry edge cases**: progress/telemetry must reflect assembled streaming deltas and multi-step retry flows; add tests that span timing/threshold behavior.
- **Use typed, canonical telemetry APIs**: prefer shared helpers/constants (and core event catalogs where applicable) over ad-hoc string event names.
- **Keep telemetry privacy-safe**: never emit raw prompts/derived hashes or other sensitive fields; use bounded property sets (and ensure telemetry capture never throws).
- **Test the telemetry contract**: unit/integration tests should assert emitted event names/props and, where relevant, trace/span status/exception presence.

Example (pattern for safe, contract-based error telemetry during retries):
```ts
onStepStart: () => {
  streamRetryBackoff?.startStep();
},
onError: async ({ error }) => {
  const captured = captureStreamError(error); // normalized error
  streamTelemetry.captureError(error);

  const wait = streamRetryBackoff?.onError(error);
  if (!wait) return;

  request.emitStatusNotice?.(
    `provider error — retrying in ${Math.round(wait.delayMs / 1000)}s (attempt ${wait.attempt}/${MODEL_STREAM_MAX_RETRIES})`,
    {
      kind: "stream_retry",
      attempt: wait.attempt,
      maxAttempts: MODEL_STREAM_MAX_RETRIES,
      delayMs: wait.delayMs,
      providerId: request.providerId,
      modelId: request.modelId,
    },
  );

  context.telemetry?.capture({
    event: CORE_TELEMETRY_EVENTS.SDK.STREAM_RETRY,
    properties: captureSdkStreamRetry(captured, { attempt: wait.attempt, delayMs: wait.delayMs }),
  });
}
```

Net effect: metrics/traces become actionable again—no wrong causes, no missing generation failures, no privacy leaks, and no silent contract drift.