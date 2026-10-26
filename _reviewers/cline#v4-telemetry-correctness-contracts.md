---
title: Telemetry Correctness Contracts
description: 'Observability is not “best effort”: treat telemetry emission as a correctness
  contract with strict semantics, timing, and payload hygiene.


  Apply this standard:'
repository: cline/cline#v4
label: Observability
language: TypeScript
comments_count: 14
repository_stars: 70864
---

Observability is not “best effort”: treat telemetry emission as a correctness contract with strict semantics, timing, and payload hygiene.

Apply this standard:

1) Use typed helpers + catalog constants (not ad-hoc strings)
- Centralize each event behind a typed helper.
- Never include sensitive/raw payloads (e.g., prompt text) in event properties.
- Write tests that assert the exact event name and exact payload shape.

Example pattern:
```ts
export const CORE_EVENTS = {
  SESSION: {
    PENDING_PROMPTS_DISCARDED: "CORE_TELEMETRY_EVENTS.SESSION.PENDING_PROMPTS_DISCARDED",
  },
} as const;

export function capturePendingPromptsDiscarded(
  telemetry: ITelemetryService | undefined,
  details: { sessionId: string; count: number; reason: "queue_abort" | "session_teardown" },
): void {
  telemetry?.capture(CORE_EVENTS.SESSION.PENDING_PROMPTS_DISCARDED, details);
}

// In host code:
capturePendingPromptsDiscarded(this.telemetry, { sessionId, count, reason });
```

2) Make reasons/classifications specific and non-inflating
- Only emit a specific metric value when the condition is truly met (e.g., real timeout vs generic ask error).
- Distinguish “empty output” from “timeout”; avoid mapping both to TIMEOUT.

3) Prevent stale attribution (reset per scope)
- If a “cause” can change across turns, clear it at the correct boundary (per turn, per lifecycle, etc.).
- Don’t inherit the previous turn’s finish reason/provider failure details for the next failure.

4) Record at the right time relative to tracing span lifecycles
- Ensure error reporting reaches the integration before the generation/model-call span closes; otherwise you’ll end up with UNSET/incorrect generation-level status.

5) Fix timer/lifecycle edge cases to avoid false samples
- If a detached observation window is used, cancel/omit the sample when spawning fails.
- Ensure timers don’t fire and report “exited:false” for never-started processes.

6) Avoid double-counting
- If tool usage/progress is already instrumented centrally, don’t re-capture in additional handlers.

7) Keep telemetry wiring side-effect free
- Telemetry configuration should not rewrite bootstrap/core state used to decide restart vs new sessions.

If you follow these rules, telemetry becomes diagnosable, trustworthy for decision gates, and safe for both dashboards and debugging workflows.