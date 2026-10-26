---
title: Avoid Duplicate Expensive Work
description: 'When code performs costly IO (git, subprocesses, network/remote inspection),
  clipboard/telemetry capture, or UI state transitions, ensure you:

  1) **Do the minimum work needed** (scope queries to upstream/default, avoid “all
  heads”/full scans when not required).'
repository: cline/cline#v23
label: Performance Optimization
language: TypeScript
comments_count: 5
repository_stars: 70889
---

When code performs costly IO (git, subprocesses, network/remote inspection), clipboard/telemetry capture, or UI state transitions, ensure you:
1) **Do the minimum work needed** (scope queries to upstream/default, avoid “all heads”/full scans when not required).
2) **Reuse already-computed results** within the same flow (don’t recapture screenshots/terminal output just to compute telemetry; derive both outputs from the single captured snapshot).
3) **Batch instead of N× subprocesses** (prefer one `git` batch call over per-file `git show`/per-entry spawning).
4) **Remove redundant logic** that re-runs checks already performed earlier in the same request.
5) **Gate expensive/UI-visible state updates** so “skip” scenarios don’t trigger unnecessary loader renders.

Example (reuse captured terminal snapshot for telemetry):
```ts
async function handleFallback() {
  const terminalSnapshot = await returnCurrentTerminalContents();
  // Use the same snapshot for both model fallback and success telemetry
  telemetryService.captureTerminalOutputFailure(
    terminalSnapshot.success ? /* reason */ undefined : TerminalOutputFailureReason.TIMEOUT,
    { snapshotId: terminalSnapshot.id }
  );
}
```

Checklist to apply in reviews:
- Are there calls that could be derived from an earlier call’s output?
- Are we looping over many items and spawning per-item subprocesses?
- Are we fetching/scanning “all” remote data when only one branch/ref is needed?
- Do skip/“provisioning”/handoff conditions still allow extra UI state changes?
- Any redundant checks that were already computed earlier in the function?
