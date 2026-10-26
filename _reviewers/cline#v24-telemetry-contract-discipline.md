---
title: Telemetry Contract Discipline
description: 'When adding or changing observability, treat telemetry as a contract:
  it must be (1) structurally valid, (2) scope-correct, and (3) operationally accurate
  (timing + attribution), or it should not be emitted.'
repository: cline/cline#v24
label: Observability
language: TypeScript
comments_count: 11
repository_stars: 70891
---

When adding or changing observability, treat telemetry as a contract: it must be (1) structurally valid, (2) scope-correct, and (3) operationally accurate (timing + attribution), or it should not be emitted.

**Rules**
1. **Use typed helpers for core/sentinel events**
   - Emit via shared, typed helper functions tied to the event catalog.
   - Property sets must be exact (no extra fields), and tests should assert both event name and property shape.
   - Respect opt-out/disablement: helpers must not call “required capture” paths when telemetry is disabled.

2. **Keep event naming scope boundaries**
   - Core telemetry: use the core catalog constants/helpers.
   - Sandbox/plugins/examples: use plugin-prefixed event names and rely on the host’s telemetry adapter/rename layer; do not force core-catalog rules onto plugin-scoped events.

3. **Reset attribution at the correct granularity**
   - Any telemetry field that’s derived per-turn (e.g., `finishReason`/cause) must be reset per turn, not per run.
   - Never allow prior-turn values to leak into later failures; “wrong cause” is worse than “missing cause”.

4. **Record before lifecycle spans close**
   - For streaming/tracing integrations, ensure the terminal error is captured early enough that generation/model-call spans receive the exception/status (avoid leaving spans UNSET).
   - If you buffer errors for later, confirm the buffered error is still available before the tracing lifecycle ends.

5. **Avoid metric pollution (false samples + misleading reasons)**
   - Do not reuse one reason value for distinct conditions (e.g., timeout vs empty-output vs ask failure). Introduce distinct stages/reasons.
   - If a sampling/observation window depends on an async action, cancel the timer on spawn/setup failure so you don’t emit a fabricated “exited:false” runtime sample.

6. **Ensure decision-phase telemetry always terminates consistently**
   - For “started/…/succeeded/failed” style events, always emit a terminal phase that matches the real outcome.
   - If a listener can throw during a “success notice”, record `failed` for the metric to prevent “success on a run that failed”.

**Code pattern (typed helper + shape/opt-out test)**
```ts
// telemetry helper
export function capturePendingPromptsDiscarded(
  telemetry: ITelemetryService | undefined,
  details: { sessionId: string; count: number; reason: "queue_abort" | "session_teardown" },
): void {
  emit(
    telemetry,
    CORE_TELEMETRY_EVENTS.SESSION.PENDING_PROMPTS_DISCARDED,
    details, // exact keys only
  );
}

// test sketch (shape + opt-out)
it("emits exact properties and respects opt-out", () => {
  const telemetry = disabledTelemetryAdapter();
  capturePendingPromptsDiscarded(telemetry, { sessionId: "s", count: 2, reason: "queue_abort" });
  expect(captureRequired).not.toHaveBeenCalled();
  // enabled case asserts event name + {sessionId,count,reason} only
});
```

If a change can’t satisfy these points (especially timing/attribution or opt-out correctness), prefer not emitting that telemetry until it can.