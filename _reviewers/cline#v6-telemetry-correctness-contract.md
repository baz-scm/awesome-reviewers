---
title: Telemetry Correctness Contract
description: 'Treat observability signals as a strict, testable contract: they must
  be (1) policy-compliant, (2) semantically accurate, (3) lifecycle-ordered, and (4)
  non-invasive to core behavior.'
repository: cline/cline#v6
label: Observability
language: TypeScript
comments_count: 11
repository_stars: 70864
---

Treat observability signals as a strict, testable contract: they must be (1) policy-compliant, (2) semantically accurate, (3) lifecycle-ordered, and (4) non-invasive to core behavior.

**Coding standard**
1) **Use typed helpers + approved event catalogs (no raw event strings in core/first-party).**
   - Centralize event emission in a helper that enforces:
     - exact catalog constant/event name
     - a fixed payload shape (no prompt text or other sensitive content)
     - compile-time constrained reason/stage values
2) **Respect telemetry opt-out by construction.**
   - Helpers must avoid any “required capture” calls when telemetry is disabled; test this.
3) **Classify metrics by the real condition.**
   - Only emit a “timeout/hang” stage when you actually have that failure mode; otherwise use an “ask_failed/ask_error” (or equivalent) stage.
4) **Avoid stale attribution: reset per-turn/per-span state early.**
   - Clear fields used to label failures (e.g., finishReason/modelFailure) at the start of the turn so previous-turn causes cannot leak.
5) **Record streaming/async errors before the corresponding span/generation observation closes.**
   - In event-driven flows, ensure pending errors are captured in `onEnd`/before model-call spans close; add tests that assert span status/exception presence.
6) **Prevent false samples.**
   - If you start an observation timer/window, ensure it is cleared/cancelled on spawn failures or other paths where “runtime” never began.
7) **Telemetry wiring must not mutate core bootstrap truth.**
   - Don’t let telemetry configuration logic rewrite session/runtime identifiers or other semantics core uses to decide restart/resume behavior.

**Pattern (typed helper + contract payload)**
```ts
// core-events.ts
export function capturePendingPromptsDiscarded(
  telemetry: ITelemetryService | undefined,
  details: {
    sessionId: string;
    count: number;
    reason: "queue_abort" | "session_teardown";
  },
): void {
  emit(telemetry, CORE_TELEMETRY_EVENTS.SESSION.PENDING_PROMPTS_DISCARDED, details);
}
```
**Pattern (lifecycle-safe capture for streaming)**
```ts
// Ensure you store the pending error when it arrives,
// but report it while the generation/span is still open.
onError() {
  failed = true;
}
onLanguageModelCallStart() {
  pendingError = undefined; // new attempt can recover
}
async onEnd(event) {
  if (event.finishReason === "error" && pendingError !== undefined) {
    await recordError(pendingError); // before spans close
  }
}
```

**Required tests (minimum)**
- Payload shape + event name constant assertions.
- Opt-out test: helper does not call required capture APIs when disabled.
- One test per “reason/stage” classification path.
- One lifecycle test for streaming/span ordering.
- One failure-path test for timer/sampling correctness.
