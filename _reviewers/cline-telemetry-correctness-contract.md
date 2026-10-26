---
title: Telemetry correctness contract
description: 'Make observability code behave like a correctness-critical contract—not
  “best effort.”


  Apply these rules:

  - **Use typed, policy-compliant helpers** for telemetry event names and payload
  shapes (never free-form event strings). Keep payloads **stable** and **bounded**;
  never emit raw prompt/text when counts/sanitized fields suffice.'
repository: Cline/Cline
label: Observability
language: TypeScript
comments_count: 16
repository_stars: 70840
---

Make observability code behave like a correctness-critical contract—not “best effort.”

Apply these rules:
- **Use typed, policy-compliant helpers** for telemetry event names and payload shapes (never free-form event strings). Keep payloads **stable** and **bounded**; never emit raw prompt/text when counts/sanitized fields suffice.
- **Respect lifecycle ordering**: if an integration/span observation may end before an error is reported, propagate/record the error early enough so terminal spans get the right status.
- **Attribute per correct scope**: initialize/reset “reason”/failure metadata at the right granularity (e.g., **per turn**, not inherited from a previous turn). Wrong causes are worse than missing ones—add tests that fail on stale attribution.
- **Classify with truthful reason codes**: reason enums must match the actual failure condition (don’t label all “ask” errors as timeouts/hangs).
- **Avoid double-counting**: instrument in one centralized place; don’t add parallel capture paths that both count the same action.
- **Don’t mutate semantic core state via telemetry wiring**: telemetry configuration should attach hooks/transport only; it must not change bootstrap/session semantics (e.g., sessionId/resume detection).
- **Test the telemetry contract**: assert event name constants, payload shape, opt-out behavior, and (where applicable) span/terminal status.

Example pattern (typed helper + bounded payload + opt-out safe):
```ts
// core-events.ts
export function capturePendingPromptsDiscarded(
  telemetry: ITelemetryService | undefined,
  details: { sessionId: string; count: number; reason: "queue_abort" | "session_teardown" },
): void {
  emit(telemetry, CORE_TELEMETRY_EVENTS.SESSION.PENDING_PROMPTS_DISCARDED, details);
}
```
