---
title: Telemetry Must Be Accurate
description: When adding or modifying observability (telemetry events, run/turn progress,
  tracing span updates), ensure the signal is (1) semantically correct, (2) correctly
  scoped to the right lifecycle boundary, (3) emitted at the right time in tracing/stream
  lifecycles, (4) not double-counted, and (5) policy-compliant—then lock it in with
  tests.
repository: cline/cline#v10
label: Observability
language: TypeScript
comments_count: 12
repository_stars: 70869
---

When adding or modifying observability (telemetry events, run/turn progress, tracing span updates), ensure the signal is (1) semantically correct, (2) correctly scoped to the right lifecycle boundary, (3) emitted at the right time in tracing/stream lifecycles, (4) not double-counted, and (5) policy-compliant—then lock it in with tests.

**Coding standards**
1. **Use typed, policy-safe event helpers**
   - Emit closed-set reason/stage values (e.g., string unions/enums).
   - Never include sensitive payloads (e.g., prompt text); capture counts/IDs instead.
   - Ensure helpers respect telemetry opt-out.

2. **Attribute causes to the correct scope**
   - Reset per-turn fields (e.g., `lastFinishReason`) at the start of each turn; never allow stale attribution from a previous turn.
   - Preserve provider details when classification rules would otherwise drop them (e.g., wrapper errors like context overflow).

3. **Emit progress signals that reflect real work**
   - If streaming tool-call argument deltas advance “activity,” reflect them in run progress; otherwise idle detection and run state telemetry can drift.

4. **Tracing timing: record terminal errors before spans end**
   - If an integration ends a generation span on a “finish”/lifecycle close, make sure the error is available before that close.
   - Tests should assert generation-level span status/exception, not just root-operation status.

5. **Avoid misclassification and double counting**
   - Don’t label generic failures as specific stages/reasons unless you can distinguish them.
   - If telemetry is already captured centrally (via an adapter/event pipeline), don’t emit a second copy in downstream handlers.

**Example pattern (policy-safe typed helper + usage)**
```ts
// telemetry helpers (policy-safe: counts/IDs only; opt-out safe)
export function capturePendingPromptsDiscarded(
  telemetry: ITelemetryService | undefined,
  details: {
    sessionId: string;
    count: number;
    reason: "queue_abort" | "session_teardown";
  },
): void {
  if (!telemetry) return;
  telemetry.capture(CORE_TELEMETRY_EVENTS.SESSION.PENDING_PROMPTS_DISCARDED, details);
}

// call site (scope-correct; no prompt text)
private discardPendingPrompts(session: ActiveSession, reason: "queue_abort" | "session_teardown") {
  const discarded = this.pendingPromptsController.discardQueue(session);
  if (discarded.length === 0) return;
  capturePendingPromptsDiscarded(this.session.config.telemetry, {
    sessionId: session.sessionId,
    count: discarded.length,
    reason,
  });
}
```

**Minimum test requirements**
- Verify the exact event name and exact property shape (IDs/counts/reason only).
- Add regression tests for: (a) stale attribution across turns, (b) streaming/threshold progress, (c) tracing span status/exception when stream errors arrive, and (d) opt-out behavior.
- For “reason/stage” metrics, add a test that distinguishes the intended conditions (and prevents generic mislabeling).