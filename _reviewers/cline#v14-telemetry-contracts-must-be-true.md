---
title: Telemetry contracts must be true
description: All observability signals must be (1) contract-compliant, (2) temporally
  correct, (3) correctly classified/attributed, (4) non-duplicative, and (5) non-interfering—especially
  under opt-out and failure/retry paths.
repository: cline/cline#v14
label: Observability
language: TypeScript
comments_count: 10
repository_stars: 70876
---

All observability signals must be (1) contract-compliant, (2) temporally correct, (3) correctly classified/attributed, (4) non-duplicative, and (5) non-interfering—especially under opt-out and failure/retry paths.

Apply these rules:
- **Use the event catalog + typed helpers (no raw strings / no ad-hoc payloads).**
  - Emit only allowed fields (e.g., counts/reasons; never prompt text).
  - Add a **shape test** asserting the event name constant and exact payload keys.
  - Add an **opt-out test** asserting required captures are skipped.
- **Report at the right time in the lifecycle.**
  - If an integration ends/flushes a span, ensure late errors are captured **before** that closes, or the generation-level spans can remain `UNSET`.
- **Make failure reasons match reality.**
  - Don’t label “TIMEOUT” when you caught a generic ask failure.
  - Add/choose reasons that reflect the actual condition.
- **Reset per-turn attribution.**
  - Clear/reset fields like finish reason / causes at the start of each turn so stale values from a previous turn can’t be attributed to the next.
- **Avoid double counting.**
  - If usage is captured centrally (runtime → adapter → handler), don’t emit the same metric again in another handler.
- **Telemetry must not change runtime bootstrap truth.**
  - Telemetry hooks must not mutate session identity/config in a way that changes core behavior.

Example (event helper + safe payload shape):
```ts
// core-events.ts
export function capturePendingPromptsDiscarded(
  telemetry: ITelemetryService | undefined,
  details: { sessionId: string; count: number; reason: "queue_abort" | "session_teardown" },
): void {
  emit(telemetry, CORE_TELEMETRY_EVENTS.SESSION.PENDING_PROMPTS_DISCARDED, details);
}

// host
private discardPendingPrompts(session: ActiveSession, reason: "queue_abort" | "session_teardown") {
  const discarded = this.pendingPromptsController.discardQueue(session);
  if (discarded.length === 0) return;
  session.config.telemetry?.capturePendingPromptsDiscarded({
    sessionId: session.id,
    count: discarded.length,
    reason,
  });
}
```

When reviewing code, require: (a) catalog/helper usage with safe payloads + shape/opt-out tests, (b) capture placement before lifecycle/span close, (c) accurate reason/cause and per-turn resets, (d) no duplicate metric emissions, and (e) no telemetry-driven mutation of session/runtime identity.