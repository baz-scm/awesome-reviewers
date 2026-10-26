---
title: Avoid redundant critical work
description: When code runs on user-visible or otherwise critical paths, avoid redundant
  or overbroad work. Prefer batching and capping external operations, reuse already-computed
  results (including for telemetry), and gate UI updates based on partial/hand-off
  state to prevent loader/render churn.
repository: cline/cline#v20
label: Performance Optimization
language: TypeScript
comments_count: 6
repository_stars: 70886
---

When code runs on user-visible or otherwise critical paths, avoid redundant or overbroad work. Prefer batching and capping external operations, reuse already-computed results (including for telemetry), and gate UI updates based on partial/hand-off state to prevent loader/render churn.

Checklist:
- Batch external commands instead of per-item spawning (e.g., prefer a single `git cat-file --batch` over `git show` in parallel).
- Cap what you fetch/scan from remote or large sets (e.g., don’t list every remote head SHA unless required; use upstream/default or a bounded ref strategy).
- Reuse computed snapshots/results for both UI and telemetry—never recapture the same expensive data twice.
- Gate UI side effects (loaders, “Thinking…” states) so partial messages during handoffs don’t cause visible churn.
- Choose timeouts defensively for real streaming behavior (don’t abort valid requests just because they don’t emit early deltas).
- If you must await under locks, mitigate perceived latency with pending UI state and coalescing.

Example (reuse snapshot once for telemetry):
```ts
async function handleFallback() {
  // Do the capture once
  const terminalSnapshot = await getLatestTerminalOutput();

  // Derive both emitted message and telemetry from the same snapshot
  telemetryService.captureTerminalOutputFailure(TerminalOutputFailureReason.TIMEOUT);
  await returnCurrentTerminalContentsFromSnapshot(terminalSnapshot);
}
```

Apply these rules during review to catch both direct bottlenecks (extra processes, duplicate captures, unbounded remote queries) and indirect performance regressions (UI churn, timeouts that trigger unnecessary retries/aborts).