---
title: Lifecycle-correct Telemetry Contracts
description: 'All telemetry/tracing instrumentation must be lifecycle-correct, truthful
  in its dimensions, privacy-safe, and enforced by tests.


  Apply this as a coding standard:'
repository: cline/cline#v17
label: Observability
language: TypeScript
comments_count: 11
repository_stars: 70883
---

All telemetry/tracing instrumentation must be lifecycle-correct, truthful in its dimensions, privacy-safe, and enforced by tests.

Apply this as a coding standard:
- **Use the approved event catalog + typed helpers**: emit via constants and helper functions with constrained union types (e.g., `reason: 'queue_abort' | 'session_teardown'`). Don’t emit raw event-name strings in core/first-party code.
- **Don’t leak sensitive content**: telemetry payloads must never include prompt/text/certs/etc. Capture only counts/identifiers and pre-sanitized properties.
- **Record outcomes at the correct lifecycle boundary**:
  - For spans, ensure the error is captured *before* the terminal generation span closes.
  - For run/turn attribution, ensure finish/reason fields are **reset per-turn** and never inherit stale values.
  - For “terminal phase” events (e.g., recovery metrics), guarantee every `started` state gets a corresponding terminal state even when listeners/hooks throw.
- **Make metric dimensions match reality**: reason/stage values must correspond to the actual condition being handled (avoid classifying “ask failure” as “stream timeout”).
- **Avoid double-counting and false samples**:
  - Use the central instrumentation pipeline; don’t re-emit the same “tool used” event in multiple handlers.
  - Cancel observation timers / stop reporting when the underlying execution didn’t actually start (e.g., spawn failure), to avoid synthetic “ran for 30s” samples.
- **Test the contract**:
  - Assert event name constants, exact payload shape, opt-out behavior (“never send when disabled”), and that sensitive fields are absent.
  - Add regression tests for attribution/timing bugs.

Example pattern (typed helper + privacy + lifecycle boundary):
```ts
// telemetry/core-events.ts
export function capturePendingPromptsDiscarded(
  telemetry: ITelemetryService | undefined,
  details: {
    sessionId: string;
    count: number;
    reason: "queue_abort" | "session_teardown";
  },
): void {
  if (!telemetry) return;
  telemetry.capture({
    event: CORE_TELEMETRY_EVENTS.SESSION.PENDING_PROMPTS_DISCARDED,
    properties: details, // no prompt text
  });
}

// host/local-runtime-host.ts
private beginTeardown(session: ActiveSession): void {
  session.shuttingDown = true;
  const discarded = this.pendingPromptsController.discardQueue(session);
  if (discarded.length) {
    capturePendingPromptsDiscarded(this.telemetry, {
      sessionId: session.id,
      count: discarded.length,
      reason: "session_teardown",
    });
  }
}
```

This standard prevents the common observability regressions shown in the discussions: missing/late error capture, stale finish causes, mislabeled timeout reasons, double-counting, and false runtime samples—all of which lead to misleading monitoring and costly investigation.