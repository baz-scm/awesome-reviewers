---
title: Causal Telemetry Contracts
description: 'Telemetry must be causally correct and lifecycle-safe: events/metrics/traces
  should represent what actually happened, with attribution reset at the right scope,
  emitted before spans close, and emitted through the approved contract (typed helpers/catalog
  + opt-out), without duplication or misclassification.'
repository: cline/cline#x
label: Observability
language: TypeScript
comments_count: 12
repository_stars: 70861
---

Telemetry must be causally correct and lifecycle-safe: events/metrics/traces should represent what actually happened, with attribution reset at the right scope, emitted before spans close, and emitted through the approved contract (typed helpers/catalog + opt-out), without duplication or misclassification.

Apply this when adding/changing observability code:

- **Use the approved telemetry contract**
  - Prefer **typed capture helpers** / **catalog constants** over raw event strings.
  - Ensure you’re going through the shared **emit/capture path** so opt-out behavior is honored.
  - Never include sensitive or unsanitized content (e.g., prompt text, hashed prompt fields) in event payloads.

- **Get attribution scope right**
  - Reset “cause” fields per correct unit (e.g., **turn vs run**) to avoid stale/misattributed failure reasons.

- **Emit at the right time for tracing**
  - For stream/tracing integrations, deliver the error **before terminal model-call/generation spans close**; otherwise you may mark the overall operation failed while leaving per-generation spans “UNSET”.

- **Always close “started” phases**
  - If you emit a `phase: "started"`, ensure you emit a terminal phase on **every** path (success, recoverable failure, unrecoverable failure, retry exhaustion, and even when telemetry listeners throw).

- **Classify failures precisely**
  - Use reason/stage values that match the actual failure mode (don’t lump empty output, ask errors, and real timeouts into a single `TIMEOUT` bucket).

- **Don’t double-count**
  - If usage/events are already emitted centrally (runtime → adapter/handler pipeline), don’t add parallel captures in downstream handlers.

- **Track progress for streaming**
  - If idleness/threshold logic depends on “progress”, ensure progress is counted for streaming chunks (e.g., tool-argument deltas), not only on coarse lifecycle events.

Example pattern (typed helper + strict reason + no sensitive payload):
```ts
// In a core telemetry module
export function capturePendingPromptsDiscarded(
  telemetry: ITelemetryService | undefined,
  properties: { sessionId: string; count: number; reason: "queue_abort" | "session_teardown" },
): void {
  emit(telemetry, CORE_TELEMETRY_EVENTS.SESSION.PENDING_PROMPTS_DISCARDED, properties);
}

// In the host code
private beginTeardown(session: ActiveSession): void {
  session.shuttingDown = true;
  this.discardPendingPrompts(session, "session_teardown");
}
```

If you follow the contract + lifecycle checklist above, you’ll avoid the common regressions shown here: wrong/missing attribution, inflated metrics, duplicated usage, and trace-generation spans left incomplete due to timing/races.