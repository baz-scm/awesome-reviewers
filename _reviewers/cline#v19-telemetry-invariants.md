---
title: Telemetry invariants
description: 'Enforce telemetry invariants so metrics/traces stay accurate, private,
  and non-regressive.


  **Rules**

  1. **Use the telemetry contract**: emit only approved catalog events via **typed
  helper(s)** (no ad-hoc raw event strings/payloads). Keep payloads strict and minimal
  (IDs/counts/reasons only).'
repository: cline/cline#v19
label: Observability
language: TypeScript
comments_count: 12
repository_stars: 70885
---

Enforce telemetry invariants so metrics/traces stay accurate, private, and non-regressive.

**Rules**
1. **Use the telemetry contract**: emit only approved catalog events via **typed helper(s)** (no ad-hoc raw event strings/payloads). Keep payloads strict and minimal (IDs/counts/reasons only).
2. **Respect opt-out/privacy**: helpers must short-circuit when telemetry is disabled; never include prompt text or hashed prompt-related fields.
3. **Record before lifecycle closes**: if you’re bridging stream/lifecycle hooks to tracing/OTel spans, ensure error/state is attached **before** the span/observation ends (otherwise generation-level spans can stay `UNSET`).
4. **Correct attribution scope**: reset “cause/reason/finishReason” at the right boundary (e.g., per turn, not per run). Wrong/stale attribution is worse than missing data.
5. **Reason/stage must match the actual condition**: don’t bucket unrelated failures into a hang/timeout reason; keep metric semantics diagnostic.
6. **No misleading samples**: clear/cancel observation timers or sampling windows on spawn/async failure paths; avoid double-counting when a central pipeline already instruments the event.
7. **Add targeted tests**: assert event names/constants, payload shape, opt-out behavior, and (when relevant) span/phase outcomes.

**Example (typed helper + strict payload)**
```ts
// core-events.ts
export function capturePendingPromptsDiscarded(
  telemetry: ITelemetryService | undefined,
  details: { sessionId: string; count: number; reason: "queue_abort" | "session_teardown" },
): void {
  if (!telemetry) return;
  // opt-out must prevent any required capture paths
  if (!telemetry.isEnabled()) return;
  emit(telemetry, CORE_TELEMETRY_EVENTS.SESSION.PENDING_PROMPTS_DISCARDED, details);
}

// caller
this.capturePendingPromptsDiscarded(telemetry, { sessionId, count, reason });
```

**Example (reset attribution per turn)**
```ts
// at start of each turn that can fail
this.state.lastFinishReason = undefined;
// then set it when a finish reason is observed for that same turn
this.state.lastFinishReason = event.reason;
```

**Example (clear timer on spawn failure)**
```ts
let timer = setTimeout(/* ... */);
try {
  const result = await completed;
  clearTimeout(timer);
  reportOnce({ durationMs: Date.now() - startedAt, exitCode: result.exitCode, exited: true });
} catch {
  clearTimeout(timer); // avoid false “exited:false” samples
  throw;
}
```