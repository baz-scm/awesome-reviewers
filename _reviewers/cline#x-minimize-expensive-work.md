---
title: Minimize Expensive Work
description: When code performs costly side effects (spawning many processes, fetching
  large remote data, clipboard/network capture, or opening remote sessions), ensure
  it runs the minimal number of times and only for the minimal scope.
repository: cline/cline#x
label: Performance Optimization
language: TypeScript
comments_count: 6
repository_stars: 70861
---

When code performs costly side effects (spawning many processes, fetching large remote data, clipboard/network capture, or opening remote sessions), ensure it runs the minimal number of times and only for the minimal scope.

Apply these rules during review:
- **No duplicate expensive calls**: if a function already fetched/produced a value (e.g., a terminal snapshot), reuse it for telemetry/UI decisions rather than calling the capture again.
- **Batch/stream external queries**: avoid per-item process spawning (e.g., don’t run `git show` for every file); prefer batch commands or single-pass listing + batch reads.
- **Limit scope for remote enumeration**: don’t fetch all remote heads/refs/history unless required; constrain to default/upstream or cached/local refs.
- **Gate side effects to the correct state**: UI loaders, rehydration, and background connections should be suppressed during known handoff/provisioning phases to avoid unnecessary render churn and extra work.
- **Warm/caches must be keyed correctly**: if pre-warming for performance, ensure it warms the exact workspace/key that the user will later use.

Example (avoid duplicate snapshot capture):
```ts
// BAD: triggers capture twice via telemetry
if (!this.fullOutput.trim()) {
  await returnCurrentTerminalContents();
  telemetry.captureTerminalOutputFailure(TerminalOutputFailureReason.TIMEOUT);
}

// BETTER: capture once and reuse
if (!this.fullOutput.trim()) {
  const snapshot = await returnCurrentTerminalContents(); // return cached snapshot
  telemetry.captureTerminalOutputFailure(TerminalOutputFailureReason.TIMEOUT, snapshot);
}
```

Outcome: fewer redundant side effects, less CPU/process churn, reduced network/IO, and smoother user-perceived performance.