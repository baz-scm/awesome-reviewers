---
title: Telemetry Lifecycle Correctness
description: All observability events/metrics/traces must be (a) correctly classified/attributed
  and (b) emitted in time for the relevant span/lifecycle to observe them.
repository: cline/cline#v8
label: Observability
language: TypeScript
comments_count: 14
repository_stars: 70867
---

All observability events/metrics/traces must be (a) correctly classified/attributed and (b) emitted in time for the relevant span/lifecycle to observe them.

Apply these rules:
1) Classify with dedicated reasons/stages (no “catch-all”).
- Only emit TIMEOUT/STREAM_TIMEOUT when it truly is that condition; otherwise add/choose a reason that matches reality (e.g., EMPTY_OUTPUT vs TIMEOUT).

2) Prevent stale attribution.
- Clear per-turn observability fields at the start of the turn; never let previous-turn fields “ride along.”
- Preserve provider details only for the failure types where they still match.

3) Emit before lifecycle/span closure.
- If an integration/observer ends generation/model-call spans on an earlier callback, ensure pending errors are recorded before the span closes; otherwise the generation spans remain UNSET/incorrect.

4) Ensure lifecycle completeness: every “started” has a deterministic “terminal”.
- If you emit a telemetry lifecycle with phase:"started", you must guarantee phase:"failed"|"succeeded"|"terminal" is recorded even when hooks/listeners throw.

5) Centralize and type telemetry contracts.
- Use typed helpers/constants for event names/properties; avoid raw event strings outside the permitted scopes.
- Avoid double counting by reusing the central instrumentation pipeline.

Example (safe lifecycle + observability timing)
```ts
// Pseudocode: ensure pending error is captured before the span/generation closes.
export function createStreamErrorTelemetry(decision) {
  let pendingError;
  return {
    onLanguageModelCallStart() {
      pendingError = undefined; // new attempt can recover
    },
    onError(chunkError) {
      pendingError = chunkError; // store, don't rely on later consumer timing
    },
    async onLanguageModelCallEnd(event) {
      if (event.finishReason === "error" && pendingError !== undefined) {
        await recordError(pendingError); // do it before spans are marked closed
      }
    },
  };
}
```

Testing checklist:
- Add regression tests that assert (1) correct reason/stage, (2) no stale fields across turns, (3) spans/generation states are marked (not UNSET) when errors occur, and (4) started->terminal telemetry always completes, even when listeners throw.