---
title: Telemetry Semantics Contract
description: 'All observability/telemetry code must follow a consistent “semantics
  contract”: events must be emitted exactly once, with correct timing/attribution,
  and with strict schemas that respect opt-out and sanitization.'
repository: CLINE/CLINE
label: Observability
language: TypeScript
comments_count: 15
repository_stars: 70837
---

All observability/telemetry code must follow a consistent “semantics contract”: events must be emitted exactly once, with correct timing/attribution, and with strict schemas that respect opt-out and sanitization.

Apply these rules when adding or changing telemetry:

1) Preserve lifecycle ordering
- If an event updates an already-ending trace/span, capture the error/status before the terminal lifecycle closes.
- Test span outcomes (e.g., generation-level exception/status) rather than only operation-level failure.

2) Keep attribution correct (no stale causes)
- Any “finish reason”/failure attribution must be reset per-turn (or per correct unit of work), not per-run.
- Recovery/phase success must be classified only when the retry actually completed cleanly.

3) Enforce telemetry policy via helpers + strict payloads
- Use central catalog constants and typed helper functions for event names and payload shapes.
- Ensure helpers never include sensitive/unneeded content (e.g., no prompt text) and never call opt-out-sensitive paths (e.g., captureRequired) when telemetry is disabled.
- Keep “catalog rule scopes” aligned with runtime context (e.g., sandboxed plugins shouldn’t be forced into core catalog rules that don’t apply).

4) Avoid double counting (single source of truth)
- Identify the one pipeline stage responsible for each metric (e.g., tool usage), and don’t re-emit in downstream handlers.
- Add regression tests that assert exact event counts.

5) Use granular, condition-accurate reasons
- Metrics like “hang”, “timeout”, and “empty output” must be distinguishable.
- If your log/method catches multiple causes, either classify them into distinct reason values or only emit when the condition truly matches.

6) Sanitize and align temporal context
- Never export sensitive data via telemetry (e.g., credentials/remotes; don’t forward stderr that can contain local paths/secrets).
- Validate that the observation window matches the intended “before/after” semantics (off-by-one mistakes happen easily).

Example pattern (typed helper + schema + opt-out safe emit):
```ts
// core-events.ts
export function capturePendingPromptsDiscarded(
  telemetry: ITelemetryService | undefined,
  details: { sessionId: string; count: number; reason: "queue_abort" | "session_teardown" },
): void {
  emit(telemetry, CORE_TELEMETRY_EVENTS.SESSION.PENDING_PROMPTS_DISCARDED, details);
}

// host/runtime usage
session.config.telemetry?.capture({
  event: CORE_TELEMETRY_EVENTS.SESSION.PENDING_PROMPTS_DISCARDED,
  ...details,
});

// tests should assert:
// - capture called once with exact catalog event name
// - payload contains only {sessionId,count,reason}
// - captureRequired is never called when telemetry is disabled
```

This contract prevents the most expensive observability failures: misleading dashboards, broken alerting due to misclassification, incorrect trace/span status due to ordering, and silent telemetry regressions from “helpful” guards or duplicated emission.