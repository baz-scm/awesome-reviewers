---
title: Typed telemetry with tests
description: Telemetry must be emitted through typed, cataloged helpers (not raw event-name
  strings) and must preserve correctness across timing, attribution, and reason codes—validated
  by automated contract tests.
repository: cline/cline#v30
label: Observability
language: TypeScript
comments_count: 9
repository_stars: 70894
---

Telemetry must be emitted through typed, cataloged helpers (not raw event-name strings) and must preserve correctness across timing, attribution, and reason codes—validated by automated contract tests.

Apply this standard when adding/changing observability in streaming, retries, recovery, and terminal/tool execution:

- Prefer typed helpers + catalog constants
  - Use shared/core helper functions for event emission so event names and payload shapes stay consistent.
  - Ensure helpers never leak sensitive content (e.g., don’t include prompt text) and only send minimal fields.
  - Verify opt-out behavior: disabled telemetry must not call “required”/expensive captures.

- Keep “reason” and “finish cause” accurate
  - Emit the closest matching enum reason; don’t reuse broad labels for distinct failure modes (e.g., don’t label empty-output as TIMEOUT).
  - Clear per-turn attribution state so failures don’t inherit prior-turn finish reasons.

- Respect span lifecycle ordering
  - If a generation/span may close early, ensure the error is recorded/observed before the terminal lifecycle ends; otherwise errors won’t attach to the right span.

- Back every telemetry change with tests
  - Assert the catalog constant used for the event name.
  - Assert payload shape exactly (and that sensitive fields are absent).
  - Assert opt-out policy (captureRequired not invoked when disabled).
  - For retry/recovery/stream errors: assert phase semantics (e.g., started → retried/failed) and that span/status assertions cover the affected generation.

Example (pattern): typed stream retry telemetry with reasoned payload and lifecycle hooks
```ts
onStepStart: () => streamRetryBackoff?.startStep(),
onError: async ({ error: streamError }) => {
  const wait = streamRetryBackoff?.onError(streamError);
  if (!wait) return;

  // Typed, catalog-backed helper usage (shape + opt-out safe)
  request.emitStatusNotice?.(
    `provider error — retrying in ${Math.round(wait.delayMs / 1000)}s (attempt ${wait.attempt}/${MODEL_STREAM_MAX_RETRIES})`,
    {
      kind: 'stream_retry',
      attempt: wait.attempt,
      maxAttempts: MODEL_STREAM_MAX_RETRIES,
      delayMs: wait.delayMs,
      providerId: request.providerId,
      modelId: request.modelId,
    },
  );

  coreEvents.captureSdkStreamRetry(telemetryService, {
    providerId: request.providerId,
    modelId: request.modelId,
    attempt: wait.attempt,
    delayMs: wait.delayMs,
    reason: 'stream_error',
  });
}
```

If you follow these rules, telemetry stays stable (names/shapes), accurate (reasons/causes), actionable (phases semantics), and correct (spans updated before closure), while remaining safe under user opt-out.