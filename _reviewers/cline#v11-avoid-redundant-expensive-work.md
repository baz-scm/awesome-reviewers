---
title: Avoid redundant expensive work
description: 'When you add “performance” logic (preflight checks, telemetry, warmups,
  hydration), treat it as a cost: avoid doing heavy work twice, scope IO/network to
  the minimum required subset, and reuse computed results.'
repository: cline/cline#v11
label: Performance Optimization
language: TypeScript
comments_count: 7
repository_stars: 70871
---

When you add “performance” logic (preflight checks, telemetry, warmups, hydration), treat it as a cost: avoid doing heavy work twice, scope IO/network to the minimum required subset, and reuse computed results.

**Rules of thumb**
- **Reuse snapshots/results**: if a function already captured output/state for user/model logic, pass that same value to telemetry/metrics instead of re-capturing.
- **Scope preflight network work**: don’t fetch/compute global state (e.g., all remote heads) when a single default/upstream ref (or local refs) is sufficient for the decision.
- **Remove duplicated validation**: if the same synchronous checks already ran, don’t run them again in another loop/branch.
- **Avoid duplicated repo reads**: consolidate shared preflight logic so the repo is read once with consistent rules.
- **Prevent unintended background connections**: hydration/list views should not trigger remote session reconnections unless the user actually opened/needs them.
- **Timeouts must match progress semantics**: ensure “first chunk”/streaming timers don’t abort legitimate long “thinking” phases where no deltas are emitted; only enforce stricter timers when you can reliably observe progress.

**Example (reuse terminal snapshot for telemetry)**
```ts
async function fallbackCaptureAndTelemetry() {
  // Capture once
  const terminalSnapshot = await getLatestTerminalOutput();

  // Use the same snapshot for fallback message + telemetry
  telemetryService.captureTerminalOutputFailure(
    terminalSnapshot ? TerminalOutputFailureReason.SUCCEEDED : TerminalOutputFailureReason.TIMEOUT
  );

  await returnCurrentTerminalContentsFromSnapshot(terminalSnapshot);
}
```

Apply the same pattern to Git/network preflights and any duplicated checks: compute once, reuse everywhere, and scope work to only what the user/action truly requires.