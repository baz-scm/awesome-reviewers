---
title: Telemetry Attribution Rules
description: 'When adding or modifying telemetry, treat it as a correctness contract—not
  best-effort logging.


  **Standards**

  1. **Use the right event source + typed helpers.**'
repository: cline/cline#v22
label: Observability
language: TypeScript
comments_count: 10
repository_stars: 70886
---

When adding or modifying telemetry, treat it as a correctness contract—not best-effort logging.

**Standards**
1. **Use the right event source + typed helpers.**
   - If the system has an event catalog rule (typed constants/helpers), don’t bypass it with ad-hoc raw event strings.
   - For plugin/sandboxed code, route through the host-provided telemetry interface and rely on host renaming/stamping rules.
2. **Prevent stale or wrong attribution.**
   - Reset/clear per-turn/per-attempt fields before any fallible work that can end a turn early.
   - Emit lifecycle/finish-reason fields in the right order so downstream “terminal” statuses can’t be made inconsistent by listener/hook behavior.
3. **Capture errors at the right time.**
   - For tracing integrations, record pending stream errors before the span/generation closes; otherwise generation-level failure annotations stay unset.
4. **Classify reasons precisely.**
   - Don’t reuse a single reason for multiple distinct failure modes (e.g., TIMEOUT vs EMPTY_OUTPUT; ask failure vs actual stream timeout). Add new enum values when needed.
5. **Make telemetry non-fatal, and lock it with tests.**
   - Telemetry capture must never break the feature.
   - Add regression tests asserting **event constants**, **phase/terminal values**, and key dimensions (finish reason, error classification, status).

**Example pattern (lifecycle + phase ordering)**
```ts
// Set per-turn attribution early to avoid cross-turn carryover.
this.state.lastFinishReason = undefined;

// When emitting a two-step lifecycle, ensure terminal-phase is captured
// before any success notice can be observed downstream.
try {
  await this.emit({ type: "status-notice", message: "...", metadata: { phase: "started" }});
  // ... do recovery work
} catch (err) {
  this.captureTaskLifecycle(EVENT, { phase: "failed", eventType: "recovery_threw" });
  throw err;
}

// Only after terminal capture, optionally emit “success” notices.
this.captureTaskLifecycle(EVENT, { phase: "succeeded" });
await this.emit({ type: "status-notice", message: "recovered", metadata: { phase: "succeeded" }});
```

Adopting these rules will prevent the most common observability failures seen in the discussions: mis-scoped events, stale attribution, missing generation-level tracing errors, inflated metrics from coarse reason labels, and regressions that silently break dashboards/decision gates.