---
title: Telemetry correctness contracts
description: 'Adopt a single standard for observability instrumentation: telemetry
  must be contract-driven (typed, cataloged, tested) and semantically correct (true
  cause, correct lifecycle timing, no stale attribution, no false samples), without
  changing runtime/bootstrapping behavior.'
repository: cline/cline#v2
label: Observability
language: TypeScript
comments_count: 15
repository_stars: 70861
---

Adopt a single standard for observability instrumentation: telemetry must be contract-driven (typed, cataloged, tested) and semantically correct (true cause, correct lifecycle timing, no stale attribution, no false samples), without changing runtime/bootstrapping behavior.

**Rules**
1) **Use centralized typed event helpers (not ad-hoc strings).**
   - Emit only catalog constant event names.
   - Payloads must be explicitly typed and schema-stable (e.g., `{ sessionId, count, reason }`), and you must not include raw prompt/text content unless explicitly allowed.
   - Add tests that assert: the exact event constant, payload shape, and opt-out behavior (e.g., required captures are not invoked when disabled).

2) **Ensure semantic accuracy of “reason/stage” and attribution.**
   - Classify the *real* cause (don’t map all ask failures to stream timeouts; don’t report TIMEOUT for empty output).
   - Clear per-turn attribution fields so later failures don’t inherit prior-turn causes.
   - For recovery/phase telemetry, treat “succeeded” only when the retry cleanly completes; ensure “started” always gets a terminal phase even on listener/throw paths.

3) **Emit at the correct lifecycle moment.**
   - For tracing/span observations, record error/terminal status before provider/lifecycle closes; otherwise downstream spans may remain UNSET.
   - Don’t double-count: if usage is recorded centrally via the runtime→adapter→handler path, don’t re-instrument the same event elsewhere.

4) **Avoid observability side effects and false samples.**
   - Cancel or guard observation timers on spawn/setup failure so you don’t report “ran for 30s” when nothing executed.
   - Telemetry observers must not mutate core bootstrap truth (e.g., don’t rewrite sessionId/config in a way that changes how the core classifies restarts).

**Example (pattern)**
```ts
// core-events.ts
export function capturePendingPromptsDiscarded(
  telemetry: ITelemetryService | undefined,
  details: { sessionId: string; count: number; reason: "queue_abort" | "session_teardown" },
): void {
  emit(telemetry, CORE_TELEMETRY_EVENTS.SESSION.PENDING_PROMPTS_DISCARDED, details);
}

// host
private beginTeardown(session: ActiveSession): void {
  session.shuttingDown = true;
  const discarded = this.pendingPromptsController.discardQueue(session);
  if (!discarded.length) return;
  capturePendingPromptsDiscarded(this.telemetry, {
    sessionId: session.id,
    count: discarded.length,
    reason: "session_teardown",
  });
}
```

**Checklist for each new telemetry change**
- Contract: typed helper + catalog constant + tested payload shape
- Policy: opt-out respected; no sensitive/raw content leaked
- Semantics: correct reason/stage; no stale attribution; no double-counting
- Timing: emitted before spans close / before terminal status is finalized
- Side effects: timers canceled; no mutation of core session/bootstrapping state