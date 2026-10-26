---
title: Accurate Telemetry Contracts
description: 'Telemetry should be correct, attributable, and timely: emit only events
  that match the real observed outcome (right unit + right reason/stage), use the
  typed event catalog/helpers (no raw strings; no sensitive fields), and record errors
  before tracing/lifecycle spans close.'
repository: cline/cline#v16
label: Observability
language: TypeScript
comments_count: 15
repository_stars: 70882
---

Telemetry should be correct, attributable, and timely: emit only events that match the real observed outcome (right unit + right reason/stage), use the typed event catalog/helpers (no raw strings; no sensitive fields), and record errors before tracing/lifecycle spans close.

Apply these rules:
1) Use typed event helpers + catalog constants
- Prefer centralized helpers that enforce event names and payload shapes.
- Avoid sending sensitive content (prompt text, hashes) in telemetry properties.
- Ensure tests assert the catalog constant (not a string).

2) Record before lifecycle closure
- For streaming/tracing, capture pending/terminal errors in the lifecycle callback that still has access to the generation span (e.g., “onEnd” before the provider/model-call end observation closes). Don’t rely on a later “onError” that can arrive after spans are already finalized.

3) Correct attribution (per turn vs per run)
- Reset “finish reason”/cause fields at the proper granularity (e.g., per turn). Don’t let a previous turn’s reason leak into a later failure path.

4) Classify reasons/stages only when true
- Don’t map every ask/IO failure to a specific stage like “STREAM_TIMEOUT.” Add dedicated reasons for distinct causes (e.g., TIMEOUT vs NO_OUTPUT/EMPTY_OUTPUT) so metrics don’t become misleading.

5) Keep observability resilient
- Telemetry must respect opt-out.
- Telemetry failures (or listener/hook throws) must not break the core action; ensure started telemetry always reaches a terminal phase (succeeded/failed) even when hooks throw.

Minimal code sketch (pattern):
```ts
// 1) Typed helper + catalog constant (no raw strings, no sensitive content)
export function capturePendingPromptsDiscarded(
  telemetry: ITelemetryService | undefined,
  props: { sessionId: string; count: number; reason: 'queue_abort'|'session_teardown' },
) {
  if (!telemetry) return;
  emit(telemetry, CORE_TELEMETRY_EVENTS.SESSION.PENDING_PROMPTS_DISCARDED, props);
}

// 2) Per-turn attribution reset
function generateAssistantMessageForTurn() {
  this.state.lastFinishReason = undefined; // reset per turn
  // ... fallible setup + streaming
}

// 3) Stream error timing: record pending error before terminal spans close
lifecycle.onEnd = async (event) => {
  if ('finishReason' in event && event.finishReason === 'error' && pendingError) {
    await recordError(pendingError); // ensure generation span gets exception
  }
};
```

If you add/modify telemetry, also add/extend tests that assert:
- the exact catalog event constants,
- phase transitions (started → terminal) and correct succeeded/failed logic,
- edge cases where ordering/attribution would otherwise be wrong (empty responses, stream error sequences, wrapped provider errors).