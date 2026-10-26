---
title: Semantically Correct Telemetry
description: When adding or changing observability/telemetry, make sure events and
  metrics are (1) semantically correct, (2) timely for the tracing lifecycle, and
  (3) non-duplicative/non-false.
repository: cline/cline#v15
label: Observability
language: TypeScript
comments_count: 7
repository_stars: 70877
---

When adding or changing observability/telemetry, make sure events and metrics are (1) semantically correct, (2) timely for the tracing lifecycle, and (3) non-duplicative/non-false.

Apply these rules:
1) Don’t misclassify failure modes
- If the condition is different, emit a different reason/stage (closed set / enum).
- Avoid catch-all mappings like “any ask error == timeout” or “empty output == timeout”.

2) Attribute only what you actually observed
- Clear per-turn/per-attempt attribution state at the start of a turn (or set it to “unknown”) so you never inherit the previous cause.
- If the stream/finish reason wasn’t reached, don’t publish the last known finish reason.

3) Record tracing errors before spans close
- If an error is “pending”, ensure it’s attached to the terminal model-call observation before the integration ends the generation span.

4) Prevent false samples from observation windows
- If a subprocess/hook never actually started (spawn/setup failed), cancel the observation timer and emit nothing for the runtime sample.

5) Avoid double counting
- Prefer central telemetry hooks/pipelines; adding local capture in the same pathway often inflates metrics.

Minimal pattern (reason enum + per-attempt attribution + safe emission timing):
```ts
// 1) Closed-set reasons match the real condition
export type TerminalOutputFailureReason =
  | "TIMEOUT"
  | "NO_OUTPUT"; // empty stdout/stderr via shell integration

function emitTerminalOutputFailure(
  telemetry: ITelemetryService | undefined,
  reason: TerminalOutputFailureReason,
) {
  if (!telemetry?.isEnabled()) return;
  telemetry.capture({ event: "terminal.output_failure", properties: { reason } });
}

// 2) Clear per-turn attribution up-front
class TelemetryAttribution {
  private lastFinishReason?: string;
  beginTurn() {
    this.lastFinishReason = undefined; // never inherit prior turn
  }
}

// 3) For tracing: attach error to the model-call observation before closing lifecycle
// (Implementation varies by stack; the key rule is ordering: record error first, then end span.)
```

Outcome: dashboards and alerts stop being misleading (no inflated metrics), root-cause analysis stays reliable (no stale/wrong causes), and tracing integrations (e.g., Langfuse/OTel) correctly mark failed generations.