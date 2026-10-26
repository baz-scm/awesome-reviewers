---
title: Telemetry contract correctness
description: 'When adding or changing observability, treat telemetry as a contract:
  it must be (1) policy-compliant, (2) lifecycle-correct, (3) semantically accurate,
  and (4) tested against opt-out and ordering edge cases.'
repository: cline/cline#v21
label: Observability
language: TypeScript
comments_count: 12
repository_stars: 70886
---

When adding or changing observability, treat telemetry as a contract: it must be (1) policy-compliant, (2) lifecycle-correct, (3) semantically accurate, and (4) tested against opt-out and ordering edge cases.

Apply these rules:
- **Use catalog/typed helpers** for core event names and payload shapes (avoid raw event strings/implicit schemas). Ensure helpers never call required-capture APIs when telemetry is opted out.
- **Never throw from telemetry**. If you capture from plugins/optional integrations, guard with `telemetry?.isEnabled()` and swallow failures.
- **Ensure ordering with tracing/lifecycle**: if an integration closes a span/generation observation, deliver the terminal error/state **before** span close (streaming/event callbacks can otherwise leave spans `UNSET`).
- **Keep attribution semantics correct**:
  - Reset per-turn attribution fields (e.g., `finishReason`) so a later failure can’t inherit a previous turn’s cause.
  - Don’t over-interpret: recovery telemetry should record what actually happened (e.g., “retried” vs “succeeded”) and avoid overreporting.
- **Use dedicated reason/stage enums** so metrics aren’t inflated/misleading (e.g., empty-output ≠ timeout; ask-error ≠ stream-timeout).
- **Avoid double-counting**: use the centralized instrumentation pipeline for tool/task usage; don’t re-capture in both adapters and handlers.
- **Lock the contract with tests**: payload shape tests, opt-out behavior tests, stale-attribution regressions, and listener/hook-throw scenarios.

Example pattern (helper + opt-out-safe + reason enum):
```ts
// Core-style helper: typed event + exact payload shape
export function capturePendingPromptsDiscarded(
  telemetry: ITelemetryService | undefined,
  details: { sessionId: string; count: number; reason: "queue_abort" | "session_teardown" },
): void {
  emit(telemetry, CORE_TELEMETRY_EVENTS.SESSION.PENDING_PROMPTS_DISCARDED, {
    sessionId: details.sessionId,
    count: details.count,
    reason: details.reason,
  });
}

// Per-turn attribution reset
function resetPerTurnTelemetryState(state: { lastFinishReason?: string }) {
  state.lastFinishReason = undefined;
}

// Semantic reason enum usage
enum TerminalOutputFailureReason { TIMEOUT, NO_OUTPUT }
// Emit NO_OUTPUT only when shell integration returned empty output
```