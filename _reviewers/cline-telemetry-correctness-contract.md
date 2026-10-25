---
title: Telemetry correctness contract
description: 'When adding or modifying telemetry, treat it like an interface with
  strict correctness guarantees:


  1) Follow the telemetry contract (naming + catalog) '
repository: CLINE/cline
label: Observability
language: TypeScript
comments_count: 11
repository_stars: 70839
---

When adding or modifying telemetry, treat it like an interface with strict correctness guarantees:

1) Follow the telemetry contract (naming + catalog) 
- Emit exactly the event names the host/runtime expects (including plugin renaming behavior) and prefer helper APIs over ad-hoc strings.
- Keep payloads constrained: only include the minimum fields needed for the decision/metric; never export prompt text or other sensitive/raw content.

2) Be opt-out- and failure-safe
- Telemetry must never break the product: guard with `telemetry?.isEnabled()` (or equivalent), and wrap captures in `try/catch`.
- Use centralized helper functions so opt-out and policy enforcement stays consistent.

3) Ensure temporal correctness for tracing
- If an error is reported from a streaming lifecycle, capture it before the terminal/closing span observation completes; otherwise you can end up with generation spans marked UNSET/missing exceptions.

4) Ensure semantic correctness (dimensions must match reality)
- Metric “reason”/stage dimensions must reflect the actual failure condition; don’t reuse a reason bucket for unrelated error types.

5) Ensure attribution correctness (reset per scope)
- Any “cause” or “finish reason” attributed to an outcome must be scoped correctly (e.g., reset per turn, not per run) so failures can’t inherit stale causes.
- If errors are wrapped, don’t rely on fragile equality checks—encode/transport the needed cause explicitly and test it.

6) Avoid double-counting and side effects
- Instrument in the single intended pipeline; don’t add additional captures in handlers that already get observed via the central event adapter/runtime flow.
- Telemetry wiring must not mutate bootstrap/runtime identity inputs that core interprets (e.g., session restart/read-only resume signals).

Illustrative pattern (opt-out-safe + constrained payload):
```ts
type Details = { sessionId: string; count: number; reason: "queue_abort" | "session_teardown" };

export function capturePendingPromptsDiscarded(
  telemetry: ITelemetryService | undefined,
  details: Details,
): void {
  if (!telemetry) return;
  if (!telemetry.isEnabled()) return;
  try {
    telemetry.capture({
      // Use the canonical catalog event name
      event: CORE_TELEMETRY_EVENTS.SESSION.PENDING_PROMPTS_DISCARDED,
      properties: details, // constrained, no prompt text
    });
  } catch {
    // Never allow telemetry to interrupt inference
  }
}
```

7) Lock it in with tests
- Assert exact event names and exact property shape.
- Add “never calls required/adapters when opt-out/disabled” tests.
- Add tracing timing tests for streaming errors (terminal generation span gets the exception/status).