---
title: Telemetry correctness and timing
description: Telemetry must be (a) policy-compliant, (b) causally correct in time,
  and (c) semantically accurate in meaning—so monitoring never turns “what happened”
  into “something close”.
repository: cline/CLINE
label: Observability
language: TypeScript
comments_count: 9
repository_stars: 70839
---

Telemetry must be (a) policy-compliant, (b) causally correct in time, and (c) semantically accurate in meaning—so monitoring never turns “what happened” into “something close”.

Apply the following standards:

1) Respect telemetry policy boundaries
- Only emit events that match the host’s catalog/renaming rules for the execution environment (e.g., sandboxed plugin vs first-party core).
- Never send raw/unapproved fields; keep payloads bounded with shape tests.
- Always honor opt-out via the telemetry service/helper layer.

2) Avoid causal ordering races
- If the integration/tracing lifecycle closes a generation/model-call span, record the error *before* that close (e.g., on terminal/end hooks that run early enough), so generation-level spans aren’t left UNSET when the operation failed.

3) Ensure semantic accuracy of “reasons” and attribution
- Emit the correct reason for the exact condition (don’t label all ask failures as stream timeouts; add dedicated stages/reasons or gate emission).
- Don’t let prior-turn causes leak into later failures (reset per-turn attribution as early as necessary).
- Don’t drop provider details for high-signal error classes; add targeted tests for regressions.

4) Lock behavior with tests that assert the telemetry contract
- Assert the exact event name and exact property set (shape), plus that helpers are not invoked when opt-out is disabled.
- Add ordering tests for “terminal error recorded before span close”.

Minimal example pattern (causal + semantic correctness):
```ts
// Bad: recording happens after a lifecycle close can already end observation.
stream.onEnd(() => {
  if (event.finishReason === "error") {
    captureError(lateError); // can arrive too late
  }
});

// Better: record the error in the hook that runs before the generation span closes.
stream.onError(() => {
  pendingError = currentError;
});
stream.onLanguageModelCallEnd(() => {
  if (pendingError) recordError(pendingError); // ensure generation span gets exception
});
```

If you’re adding/changing telemetry, ask:
- “What exact condition produced this reason?”
- “Can any earlier-turn value leak here?”
- “Will this be recorded before the relevant span closes?”
- “Does the payload match the allowed shape and honor opt-out?”