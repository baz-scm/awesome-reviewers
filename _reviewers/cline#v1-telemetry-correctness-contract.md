---
title: Telemetry correctness contract
description: 'Adopt a single observability contract for every telemetry/metrics change:
  emit the right event with the right (safe) payload at the right time, without interfering
  with the runtime’s control flow.'
repository: cline/cline#v1
label: Observability
language: TypeScript
comments_count: 11
repository_stars: 70862
---

Adopt a single observability contract for every telemetry/metrics change: emit the right event with the right (safe) payload at the right time, without interfering with the runtime’s control flow.

**Rules**
1. **Use typed, cataloged helpers (no raw event strings in core):** Route captures through first-party helper functions that enforce the correct event name and payload shape. Never include prompt/tool text unless the contract explicitly allows it.
2. **Respect opt-out everywhere:** If the telemetry adapter is disabled, helper functions must not call opt-in/required-capture mechanisms that assume enabled state.
3. **Lifecycle timing:** If a span/observation can close before an error is observed, capture the error in the earlier lifecycle hook (the one that still has the error) so traces aren’t left with UNSET/failed-at-root but succeeded-at-generation.
4. **No stale attribution:** Per-turn failure/finishReason (or similar causes) must be cleared/reset at the correct boundary. Avoid carrying previous-turn causes into later failures.
5. **Correct classification granularity:** Metric “reason”/“stage” values must match the actual condition (e.g., distinguish empty output vs real timeout; don’t label all ask failures as a timeout hang).
6. **Single source of truth / no double counting:** Prefer centralized instrumentation already owned by the run loop/adapters. Avoid adding additional capture points that cause duplicate events.
7. **Non-interference:** Observability code must not mutate bootstrap/session truth (e.g., rewriting sessionId during telemetry hook setup). Attach hooks, don’t change what core considers “startup identity.”

**Example pattern (typed helper + safe payload)**
```ts
// core-events.ts
export const CORE_TELEMETRY_EVENTS = {
  SESSION: {
    PENDING_PROMPTS_DISCARDED: "core.session.pending_prompts_discarded",
  },
} as const;

export function capturePendingPromptsDiscarded(
  telemetry: ITelemetryService | undefined,
  details: { sessionId: string; count: number; reason: "queue_abort" | "session_teardown" },
): void {
  emit(telemetry, CORE_TELEMETRY_EVENTS.SESSION.PENDING_PROMPTS_DISCARDED, details);
}

// host
private discardPendingPrompts(session: ActiveSession): void {
  const discarded = this.pendingPromptsController.discardQueue(session);
  if (discarded.length === 0) return;
  capturePendingPromptsDiscarded(this.telemetry, {
    sessionId: session.id,
    count: discarded.length,
    reason: "session_teardown",
  });
}
```

**Tests to require**
- Payload shape tests (exact keys, no unsafe fields).
- Opt-out/adapter disabled tests.
- Timing-sensitive tests (stream retries, span closure, late error delivery).
- Stale-attribution regression tests across multi-turn runs.
- Reason/stage accuracy tests for “empty output vs timeout” and “hang vs non-hang” classifications.