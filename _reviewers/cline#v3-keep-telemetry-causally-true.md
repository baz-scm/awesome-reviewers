---
title: Keep telemetry causally true
description: 'Telemetry should be causally and temporally correct: set/clear attribution
  fields per the true scope (turn vs run), classify metric reasons based on the actual
  condition, and emit errors early enough for trace integrations to mark terminal
  spans before lifecycles close. Enforce the telemetry contract (typed event helpers,
  fixed payload shape, no sensitive...'
repository: cline/cline#v3
label: Observability
language: TypeScript
comments_count: 14
repository_stars: 70863
---

Telemetry should be causally and temporally correct: set/clear attribution fields per the true scope (turn vs run), classify metric reasons based on the actual condition, and emit errors early enough for trace integrations to mark terminal spans before lifecycles close. Enforce the telemetry contract (typed event helpers, fixed payload shape, no sensitive content, opt-out-safe behavior) with regression tests so telemetry can’t silently regress.

Practical rules:
- **Attribution scope**: reset fields like `finishReason`/failure causes per turn; never let a previous turn’s reason “stick”.
- **Reason correctness**: don’t label a broad `catch` as a specific timeout/hang—emit a dedicated reason that matches the condition (or emit nothing).
- **Trace timing**: if you buffer/pending-capture stream errors, ensure the error is recorded *before* the generation/lifecycle span closes.
- **No double-counting**: instrument in one central pipeline; downstream handlers should not re-capture the same semantic event.
- **Contract enforcement**: use typed catalog helpers for core events (fixed event name + payload fields) and test opt-out behavior; never include prompt/text content.

Example pattern (typed core helper + correct reason):
```ts
// core-events.ts
export function capturePendingPromptsDiscarded(
  telemetry: ITelemetryService | undefined,
  details: { sessionId: string; count: number; reason: "queue_abort" | "session_teardown" },
): void {
  emit(telemetry, CORE_TELEMETRY_EVENTS.SESSION.PENDING_PROMPTS_DISCARDED, details);
}

// host
private discardPendingPrompts(session: ActiveSession, reason: "queue_abort"|"session_teardown") {
  const discarded = this.pendingPromptsController.discardQueue(session);
  if (discarded.length === 0) return;
  session.config.telemetry?.capturePendingPromptsDiscarded({
    sessionId: session.sessionId,
    count: discarded.length,
    reason,
  });
}

// metric reason: only emit TIMEOUT when it actually is a timeout
try {
  await this.ask("command_output", chunk);
} catch (e) {
  if (isTimeoutError(e)) {
    telemetryService.captureTerminalHang(TerminalHangStage.TIMEOUT);
  } else {
    telemetryService.captureTerminalHang(TerminalHangStage.ASK_ERROR);
  }
}
```

When you change telemetry logic, add/adjust tests to lock in: (1) exact event names/payload shape, (2) opt-out behavior, and (3) timing/ordering assumptions (e.g., terminal spans get exceptions).